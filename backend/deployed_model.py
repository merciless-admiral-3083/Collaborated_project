# backend/deployed_model.py
import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

BASE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "ml", "regressor.pkl")
# optional embedder for text -> features
EMBEDDER = None
try:
    EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    EMBEDDER = None

_model = None
def _load():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def explain_score(score):
    if score < 30:
        return "Low risk"
    elif score < 60:
        return "Moderate risk"
    else:
        return "High risk"

def predict_from_features(features: dict):
    """
    features: dict expected keys:
      news_negative_pct, keyword_score, weather_risk, port_delay_index, supplier_concentration, hist_delay
    """
    model = _load()
    # ensure order match training
    order = ["news_negative_pct", "keyword_score", "weather_risk", "port_delay_index", "supplier_concentration", "hist_delay"]
    x = [features.get(k, 0.0) for k in order]
    pred = model.predict([x])[0]
    pred = float(max(0, min(100, pred)))
    return {"risk_score": round(pred,2), "status": explain_score(pred)}

def predict_text(text: str, extras: dict = None):
    """
    Convenience function: convert text to simple features (sentiment, keyword counts) then predict.
    extras: optional dictionary to provide port_delay_index etc.
    """
    extras = extras or {}
    # naive text features: negative sentiment pct (TextBlob) + keyword hits
    try:
        from textblob import TextBlob
        sentiment = TextBlob(text).sentiment.polarity
        # negative polarity -> convert to percentage
        news_negative_pct = max(0.0, -sentiment*100)
    except Exception:
        news_negative_pct = 10.0
    # simple keyword score
    kw_list = ["strike","delay","congestion","shortage","conflict","sanction","flood","earthquake","shutdown","protest","blockade"]
    kscore = 0
    t = text.lower() if text else ""
    for kw in kw_list:
        if kw in t:
            kscore += 10
    features = {
        "news_negative_pct": news_negative_pct,
        "keyword_score": kscore,
        "weather_risk": extras.get("weather_risk", 0),
        "port_delay_index": extras.get("port_delay_index", 5),
        "supplier_concentration": extras.get("supplier_concentration", 0.3),
        "hist_delay": extras.get("hist_delay", 5)
    }
    return predict_from_features(features)
