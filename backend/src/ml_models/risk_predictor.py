# backend/src/ml_models/risk_predictor.py
<<<<<<< HEAD

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
=======
from typing import List, Dict

RISK_KEYWORDS = {
    "war": 25,
    "conflict": 20,
    "protest": 10,
    "shortage": 15,
    "delay": 15,
    "flood": 18,
    "earthquake": 22,
    "sanction": 12,
    "policy": 8,
    "inflation": 10,
}

def compute_risk_from_news(articles: List[Dict]) -> Dict:
    """
    Deterministic risk scoring from list of articles.
    Returns stable fields used by frontend:
      - risk_score (0-100)
      - status ("Low risk"/"Moderate risk"/"High risk")
      - risk_label (shorter label)
      - explanation (human friendly)
      - top_risk_factors (list of "kw (+weight)")
      - top_articles (first 5 articles)
    """
    if not articles:
        return {
            "risk_score": 10,
            "status": "Low risk",
            "risk_label": "Low",
            "explanation": "No relevant news found — low current risk.",
            "top_risk_factors": [],
            "top_articles": [],
        }

    # Count matches and accumulate weighted score
    score = 0
    keyword_hits = {}
    for a in articles:
        title = (a.get("title") or "").lower()
        desc = (a.get("description") or "").lower()
        text = f"{title} {desc}"
        for kw, w in RISK_KEYWORDS.items():
            if kw in text:
                score += w
                keyword_hits[kw] = keyword_hits.get(kw, 0) + w

    # Heuristic normalization: scale to 0-100 based on max plausible sum
    # max per article if many keywords matched could be large; we normalize by number of articles
    max_per_article = max(RISK_KEYWORDS.values()) * 2  # rough upper bound
    normalized = int(min(100, (score / (len(articles) * max_per_article)) * 100 * 0.9 + 10))
    # clamp
    normalized = max(0, min(100, normalized))

    # status / labels
    if normalized >= 75:
        status = "High risk"
        label = "High"
    elif normalized >= 40:
        status = "Moderate risk"
        label = "Moderate"
    else:
        status = "Low risk"
        label = "Low"

    # build explanation
    if keyword_hits:
        # sort by weight contribution
        sorted_factors = sorted(keyword_hits.items(), key=lambda x: -x[1])
        top_factors = [f"{k} (+{v})" for k, v in sorted_factors[:5]]
        explanation = (
            f"Detected {sum(keyword_hits.values())} weighted keyword hits. "
            f"Top factors: {', '.join([k for k,_ in sorted_factors[:3]])}."
        )
    else:
        top_factors = []
        explanation = "No strong risk keywords detected in recent articles."

    # ensure top_articles safe copy
    top_articles = articles[:5]

    return {
        "risk_score": normalized,
        "status": status,
        "risk_label": label,
        "explanation": explanation,
        "top_risk_factors": top_factors,
        "top_articles": top_articles,
>>>>>>> b48960ecb6bddf285a4dd79f10af719c55c4c8f6
    }
