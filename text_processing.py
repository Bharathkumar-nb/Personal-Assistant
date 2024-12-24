import redis
import os
import requests
import datetime
import time

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

vllm_host = os.getenv('VLLM_HOST', 'localhost')
vllm_port = os.getenv('VLLM_PORT', 8000)

print("text_processing started", flush=True)

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
        print(f"Error processing text: {e}")
        return "Network Error"
    
    # Parse the response
    result = response.json()
    return result.get('choices', [])[0].get('message', {}).get('content', '')

print("Waiting on transciption", flush=True)
while True:
    # Retrieve text from Redis queue
    data = redis_client.blpop('transcriptions', timeout=30)
    print(f"{data}", flush=True)
    if data:
        text, data = data  # Unpack only if data is not None
        start_time = time.time()
        processed_text = process_text(data.decode('utf-8'))
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"AI response - {processed_text}; time {processing_time:.2f} seconds.", flush=True)
        # Publish the processed text to Redis queue
        redis_client.rpush('assistant_response', processed_text)
print("text_processing Exiting", flush=True)
