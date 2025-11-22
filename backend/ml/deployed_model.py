import pickle
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import joblib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load embedder
embedder_name_path = os.path.join(BASE_DIR, "embedder_name.txt")
with open(embedder_name_path, "r") as f:
    EMBEDDER_NAME = f.read().strip()

embedder = SentenceTransformer(EMBEDDER_NAME)

# Load trained regressor
model_path = os.path.join(BASE_DIR, "regressor.pkl")
regressor = joblib.load("backend/ml/regressor.pkl")


def predict_text(text: str):
    """Return ML-predicted risk score."""
    emb = embedder.encode([text])
    pred = regressor.predict(emb)[0]
    
    pred = float(max(0, min(100, pred)))  # clamp 0–100

    if pred < 30:
        status = "Low risk"
    elif pred < 60:
        status = "Moderate risk"
    else:
        status = "High risk"

    return {
        "risk_score": pred,
        "status": status,
        "risk_label": status
    }
