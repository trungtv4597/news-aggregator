from newsapi import NewsApiClient
from dotenv import load_dotenv
# import json
# from datetime import datetime
import os

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def fetch_articles(topic=None) -> list:
    """
    Fetch articles and save them in a structured format.
    Best Practies:
        - Rate Limit: NewsAPI's free tier has limits. Use <page_size> to fetch up to 100 articles per request and avoid hitting limits.
        - Why JSON: It's lightweight, human-readable, and widly supported.
    """
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    # Fetech top headlines
    try:
        if topic:
            articles_response = newsapi.get_everything(
                q=topic, 
                language="en", 
                sort_by="publishedAt",
                page_size=10
            )
        else:
            articles_response = newsapi.get_top_headlines(
                language="en",
                page_size=10
            )
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []

    articles = articles_response.get("articles", [])
    for article in articles:
        article["topic"] = topic
        
    if len(articles) < 1:
        logger.error(f"Couldn't find any article related to {topic}")
        return []

    # # Save raw data to JSON
    # os.makedirs(ARTICLES_STORE, exist_ok=True)
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # new_file = f"{ARTICLES_STORE}news_{timestamp}.json"

    # with open(new_file, "w", encoding="utf-8") as f:
    #     json.dump(articles["articles"], f, ensure_ascii=False, indent=2)

    # print(f"Saved {len(articles["articles"])} articles to {ARTICLES_STORE}")

    logger.info(f"Fetched {len(articles)} articles for topic {topic}")
    return articles

if __name__ == "__main__":
    topic = input("Input your topic: ")
    articles = fetch_articles(topic=topic.strip().lower())
    print(f"Fetch Articles: {articles}")