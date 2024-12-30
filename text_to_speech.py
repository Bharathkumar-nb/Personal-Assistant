import pyttsx3
import redis
import time
import signal
import os
import logging

# Ensure the directories exists
os.makedirs('/app/logs', exist_ok=True)

logger = logging.getLogger('text_processing')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('/app/logs/app_tts.log')
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

keep_running = True

def signal_handler(sig, frame):
    global keep_running
    logger.info(f"\nSignal {sig} received, stopping text-to-speech service...")
    keep_running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)

# Initialize the pyttsx3 engine globally
engine = pyttsx3.init()

def text_to_speech(text):
    logger.info(text)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    logger.info("Text-to-Speech service is running. Use 'kill -SIGUSR1 <PID>' to stop.")

    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))

    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    logger.info("Flushing redis database")
    redis_client.flushdb()

    while keep_running:
        try:
            text = redis_client.lpop('assistant_response')
            if text:
                text_to_speech(text.decode('utf-8'))
            time.sleep(1)
        except EOFError:
            break

    logger.info("Text-to-Speech service stopped.")
