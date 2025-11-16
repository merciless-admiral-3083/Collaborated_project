# backend/src/ml_models/risk_predictor.py

from typing import List, Dict
from textblob import TextBlob

RISK_KEYWORDS = {
    "strike": 15,
    "protest": 12,
    "conflict": 14,
    "shortage": 18,
    "inflation": 10,
    "violence": 20,
    "war": 25,
    "sanction": 12,
    "flood": 14,
    "earthquake": 16,
    "political": 10,
    "blockade": 22,
    "port congestion": 20,
    "delay": 15,
    "disruption": 18,
    "shutdown": 20,
}

def compute_risk_from_news(articles: List[Dict]) -> Dict:
    total_score = 0
    factors = []
    top_articles = []

    for article in articles:
        text = (article.get("title") or "") + " " + (article.get("description") or "")
        text_lower = text.lower()

        # --- 1) Key-word based scoring ---
        for word, weight in RISK_KEYWORDS.items():
            if word in text_lower:
                total_score += weight
                factors.append(f"{word} (+{weight})")

        # --- 2) Sentiment scoring ---
        sentiment = TextBlob(text).sentiment.polarity
        if sentiment < -0.3:
            score = abs(sentiment) * 20
            total_score += score
            factors.append(f"Negative sentiment ({sentiment:.2f})")

        # save article
        top_articles.append(article)

    # Normalize score
    risk_score = min(total_score, 100)

    # Categorize risk
    if risk_score > 70:
        status = "High risk"
    elif risk_score > 40:
        status = "Moderate risk"
    else:
        status = "Low risk"

    return {
        "risk_score": round(risk_score, 2),
        "status": status,
        "top_risk_factors": factors[:5],
        "top_articles": top_articles[:5],
    }
