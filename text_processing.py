import redis
import os
import requests
import datetime
import time

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

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
    
    # Send a request to the text generation service
    response = requests.post(
        'http://localhost:8000/v1/chat/completions',
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    # Parse the response
    result = response.json()
    return result.get('choices', [])[0].get('message', {}).get('content', '')

while True:
    # Retrieve text from Redis queue
    text = redis_client.lpop('transcriptions')
    if text:
        start_time = time.time()
        processed_text = process_text(text.decode('utf-8'))
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"AI response - {processed_text}; time {processing_time:.2f} seconds.", flush=True)
        # Publish the processed text to Redis queue
        redis_client.rpush('assistant_response', processed_text)
