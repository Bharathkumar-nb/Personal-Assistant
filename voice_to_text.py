import whisper
import sounddevice as sd
import numpy as np
import wavio
import signal
import sys
import warnings
import datetime
import time
import multiprocessing as mp
import os
import redis
import logging

# Ensure the directories exists
os.makedirs('/app/logs', exist_ok=True)
os.makedirs('/app/audio_files', exist_ok=True)

logger = logging.getLogger('voice_to_text')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('/app/logs/app_vtt.log')
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Add formatters to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Ignore warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
warnings.filterwarnings("ignore", message="Performing inference on CPU when CUDA is available")
warnings.filterwarnings("ignore", category=FutureWarning)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
# Initialize Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

logger.info("Flushing redis database")
redis_client.flushdb()

# Flag to indicate if the program should continue running
keep_running = True

def transcribe_audio(audio_queue, process_id):
    logger.info(f"Process {process_id} started.")
    # Changed to CPU as GPU is used for text-processing
    model = whisper.load_model("medium", device="cpu")
    logger.info(f"Process {process_id} model loaded.")
    while True:
        audio_file = audio_queue.get()
        if audio_file is None:
            logger.error(f"Process {process_id} received termination signal.")
            break  # Exit the loop if a None value is received
        start_time = time.time()
        result = model.transcribe(audio_file)
        end_time = time.time()
        processing_time = end_time - start_time
        if result["text"].strip()\
              and "Thanks for watching" not in result["text"]\
              and "Thank you" not in result["text"]:
            redis_client.rpush('transcriptions', result["text"])
            logger.info(f"[{datetime.datetime.now()}] audiofile: {audio_file} {result['text']}")
        os.remove(audio_file)  # Remove the audio file after transcription to save space

def record_audio_segment(segment_duration, sample_rate=16000):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    audio_file = f"/app/audio_files/segment_{timestamp}.wav"
    audio = sd.rec(int(segment_duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    start_time = time.time()
    wavio.write(audio_file, audio, sample_rate, sampwidth=2)
    end_time = time.time()
    processing_time = end_time - start_time
    return audio_file

def signal_handler(sig, frame):
    global keep_running
    logger.info("\nSignal handler called, stopping continuous audio capture...")
    keep_running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    segment_duration = 10  # Duration of each segment in seconds
    logger.info("Use kill -SIGINT <PID> to stop the recording.")
    
    logger.info("Loading Whisper models...")
    manager = mp.Manager()
    audio_queue = manager.Queue()
    
    # Precreate multiple processes with loaded Whisper models
    processes = []
    for i in range(2):  # Adjust the number of processes if needed
        p = mp.Process(target=transcribe_audio, args=(audio_queue, i))
        processes.append(p)
        p.start()
    
    logger.info("Whisper models loaded and processes started successfully.")

    while keep_running:
        segment_file = record_audio_segment(segment_duration)
        
        # Add the audio segment to the audio queue
        audio_queue.put(segment_file)

    # Stop all processes by sending None to the audio queue
    for _ in processes:
        audio_queue.put(None)
    
    # Ensure all processes finish
    for p in processes:
        p.join()

    print("Exited the recording loop.")
