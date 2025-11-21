# backend/src/ml_models/risk_predictor.py
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
    }
