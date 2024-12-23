import pyttsx3
import redis
import time
import signal
import os

keep_running = True

def signal_handler(sig, frame):
    global keep_running
    print(f"\nSignal {sig} received, stopping text-to-speech service...", flush=True)
    keep_running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("Text-to-Speech service is running. Use 'kill -SIGUSR1 <PID>' to stop.", flush=True)

    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))

    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    while keep_running:
        try:
            text = redis_client.lpop('transcriptions')
            if text:
                text_to_speech(text.decode('utf-8'))
            time.sleep(1)
        except EOFError:
            break

    print("Text-to-Speech service stopped.", flush=True)
