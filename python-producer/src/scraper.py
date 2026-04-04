import time
import json
import os
import feedparser
import redis
from schemas import NewsAlert

RSS_FEED_URL = "https://finance.yahoo.com/news/rss"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

print(f"Connecting to Redis at: {REDIS_HOST}:{REDIS_PORT}...", flush=True)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def fetch_latest_news():
    print(f"Fetching latest news from {RSS_FEED_URL}...", flush=True)
    feed = feedparser.parse(RSS_FEED_URL)
    
    for entry in feed.entries[:3]:
        try:
            alert = NewsAlert(
                headline = entry.title,
                impact_score = 0.5, # dummy for now, since LLM is not implemented yet
                category = "Finance"
            )
            
            alert_json = alert.model_dump_json() # convert Pydantic object to JSON
            redis_client.lpush("news_queue", alert_json) # pushing it to the Redis queue
            print(f"Sent to Redis: {alert.headline}", flush=True)
            
        except Exception as e:
            print(f"Pydantic validation error: {e}", flush=True)

if __name__ == "__main__":
    print("Sentinel Python Container Started!", flush=True)
    while True:
        fetch_latest_news()
        print("Sleeping for 60 seconds before next fetch...", flush=True)
        time.sleep(60)