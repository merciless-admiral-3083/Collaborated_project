# backend/src/data_ingestion/fetch_news.py

import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

NEWSAPI_URL = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # now correctly loaded


def fetch_news_for_country(country: str, page_size: int = 10, api_key: str = None) -> List[Dict]:
    """
    Fetch recent news articles for a country.
    Uses NewsAPI if API key exists, otherwise returns mocked sample data.
    """

    # If caller passed custom key, override default
    key = api_key or NEWSAPI_KEY

    # No API key → return mock data
    if not key:
        print("⚠️ NEWSAPI_KEY missing — using mock data.")
        return [
            {
                "title": f"Port congestion rising in {country}",
                "description": "Ships experiencing delays.",
                "source": "MockNews",
                "published_at": None,
                "url": None
            },
            {
                "title": f"Strike at major {country} seaport disrupts shipments",
                "description": "Workers halt operations for 48 hours.",
                "source": "MockNews",
                "published_at": None,
                "url": None
            },
            {
                "title": f"{country} trade deal eases shipping bottlenecks",
                "description": "New policy expected to reduce delays.",
                "source": "MockNews",
                "published_at": None,
                "url": None
            }
        ]

    # Real API call
    params = {
        "q": country,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": key,
    }

    try:
        resp = requests.get(NEWSAPI_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return []

    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a.get("title") or "",
            "description": a.get("description") or "",
            "source": (a.get("source") or {}).get("name", "Unknown"),
            "published_at": a.get("publishedAt"),
            "url": a.get("url"),
        })

    return articles
