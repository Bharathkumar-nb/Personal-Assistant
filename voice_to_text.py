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

# Ignore FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Flag to indicate if the program should continue running
keep_running = True

def transcribe_audio(audio_queue, result_queue, process_id):
    print(f"Process {process_id} started.", flush=True)
    model = whisper.load_model("medium")
    print(f"Process {process_id} model loaded.", flush=True)
    while True:
        #print(f"Process {process_id} waiting for audio file...", flush=True)
        audio_file = audio_queue.get()
        if audio_file is None:
            print(f"Process {process_id} received termination signal.", flush=True)
            break  # Exit the loop if a None value is received
        #print(f"Process {process_id} received file {audio_file} for transcription.", flush=True)
        start_time = time.time()
        result = model.transcribe(audio_file)
        end_time = time.time()
        processing_time = end_time - start_time
        #print(f"Process {process_id} completed transcription in {processing_time:.2f} seconds.", flush=True)
        result_queue.put(result["text"])
        redis_client.rpush('transcriptions', result["text"])
        os.remove(audio_file)  # Remove the audio file after transcription to save space
        #print(f"Process {process_id} added transcription result to result_queue.", flush=True)

def record_audio_segment(segment_duration, sample_rate=16000):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    audio_file = f"/app/segment_{timestamp}.wav"
    audio = sd.rec(int(segment_duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    start_time = time.time()
    wavio.write(audio_file, audio, sample_rate, sampwidth=2)
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"record_audio_segment completed saving segment in {processing_time:.2f} seconds.", flush=True)
    return audio_file

def signal_handler(sig, frame):
    global keep_running
    print("\nSignal handler called, stopping continuous audio capture...", flush=True)
    keep_running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)

if __name__ == "__main__":
    segment_duration = 10  # Duration of each segment in seconds
    print("Use kill -SIGINT <PID> to stop the recording.", flush=True)
    
    print("Loading Whisper models...", flush=True)
    manager = mp.Manager()
    audio_queue = manager.Queue()
    result_queue = manager.Queue()
    
    # Precreate multiple processes with loaded Whisper models
    processes = []
    for i in range(2):  # Adjust the number of processes if needed
        p = mp.Process(target=transcribe_audio, args=(audio_queue, result_queue, i))
        processes.append(p)
        p.start()
    
    print("Whisper models loaded and processes started successfully.", flush=True)

    while keep_running:
        #print("Starting a new recording segment...", flush=True)
        segment_file = record_audio_segment(segment_duration)
        #print(f"Recording segment completed, adding {segment_file} to queue for transcription...", flush=True)
        
        # Add the audio segment to the audio queue
        audio_queue.put(segment_file)
        #print(f"Added {segment_file} to audio_queue.", flush=True)
        
        # Print transcriptions as they complete
        while not result_queue.empty():
            transcription = result_queue.get()
            print(f"[{datetime.datetime.now()}] {transcription}", flush=True)
        
        #print("Transcription process is ongoing.", flush=True)

    # Stop all processes by sending None to the audio queue
    for _ in processes:
        audio_queue.put(None)
    
    # Ensure all processes finish
    for p in processes:
        p.join()

    print("Exited the recording loop.", flush=True)
