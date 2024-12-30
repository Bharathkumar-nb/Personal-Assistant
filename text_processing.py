import redis
import os
import requests
import datetime
import time
import logging

# Ensure the directories exists
os.makedirs('/app/logs', exist_ok=True)

logger = logging.getLogger('text_processing')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('/app/logs/app_tp.log')
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

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

logger.info("Flushing redis database")
redis_client.flushdb()

vllm_host = os.getenv('VLLM_HOST', 'localhost')
vllm_port = os.getenv('VLLM_PORT', 8000)

logger.info("text_processing started")

def process_text(text):
    # Request payload
    payload = {
        "model": "llm",
        "messages": [
            {"role": "system", "content": "You are a friend."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    try:
        # Send a request to the text generation service
        response = requests.post(
            f"http://{vllm_host}:{vllm_port}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload
        )
    except (requests.exceptions.RequestException, ConnectionError) as e:
        logger.error(f"Error processing text: {e}")
        return "Network Error"
    
    # Parse the response
    result = response.json()
    return result.get('choices', [])[0].get('message', {}).get('content', '')

logger.info("Waiting on transciption")
while True:
    # Retrieve text from Redis queue
    data = redis_client.blpop('transcriptions', timeout=30)
    logger.info(f"{data}")
    if data:
        text, data = data  # Unpack only if data is not None
        start_time = time.time()
        processed_text = process_text(data.decode('utf-8'))
        end_time = time.time()
        processing_time = end_time - start_time
        logger.info(f"AI response to {data.decode('utf-8')} - {processed_text}; time {processing_time:.2f} seconds.")
        if processed_text != "Network Error":
            # Publish the processed text to Redis queue
            redis_client.rpush('assistant_response', processed_text)
logger.info("text_processing Exiting")
