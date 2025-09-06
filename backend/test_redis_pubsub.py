import redis
import asyncio
import threading
import time

# --- Configuration ---
# Make sure this matches your .env file exactly
REDIS_URL = "redis://localhost:6379/0"

# --- Subscriber (Listener) ---
def subscriber():
    print("[Subscriber] Thread started. Connecting to Redis...")
    r = redis.from_url(REDIS_URL, decode_responses=True)
    p = r.pubsub()
    p.psubscribe("log_channel:*")
    print("[Subscriber] Subscribed to 'log_channel:*'. Waiting for messages...")
    
    for message in p.listen():
        if message['type'] == 'pmessage':
            print(f"✅ [Subscriber] SUCCESS! Received on channel '{message['channel']}': {message['data']}")

# --- Publisher (Sender) ---
def publisher():
    print("[Publisher] Thread started. Connecting to Redis...")
    r = redis.from_url(REDIS_URL, decode_responses=True)
    test_task_id = "test-12345"
    channel = f"log_channel:{test_task_id}"
    
    print("\n--- Running Test ---")
    time.sleep(2) # Give subscriber time to connect
    
    print(f"[Publisher] Publishing 'Hello World' to channel '{channel}'...")
    r.publish(channel, "Hello World")
    
    time.sleep(1)
    
    print(f"[Publisher] Publishing 'Test Complete' to channel '{channel}'...")
    r.publish(channel, "Test Complete")
    print("[Publisher] Test finished.")


if __name__ == "__main__":
    # Run subscriber in a background thread
    subscriber_thread = threading.Thread(target=subscriber, daemon=True)
    subscriber_thread.start()
    
    # Run publisher in the main thread
    publisher()