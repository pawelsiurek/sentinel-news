import time
import feedparser
from schemas import NewsAlert

RSS_FEED_URL = "https://finance.yahoo.com/news/rss"

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
            print(f"Correctly validated: {alert.headline}", flush=True)
        except Exception as e:
            print(f"Pydantic validation error: {e}", flush=True)

if __name__ == "__main__":
    print("Sentinel Python Container Started!", flush=True)
    while True:
        fetch_latest_news()
        print("Sleeping for 60 seconds before next fetch...", flush=True)
        time.sleep(60)