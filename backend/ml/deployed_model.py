import os
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load embedder name
embedder_name_path = os.path.join(BASE_DIR, "embedder_name.txt")
with open(embedder_name_path, "r") as f:
    EMBEDDER_NAME = f.read().strip()

# Load embedder model
embedder = SentenceTransformer(EMBEDDER_NAME)

# Load trained regressor
model_path = os.path.join(BASE_DIR, "regressor.pkl")
regressor = joblib.load(model_path)


def predict_text(text: str):
    """Return ML-predicted risk score."""

    # Empty text protection
    if not text or not text.strip():
        return {
            "risk_score": 10,
            "status": "Low risk",
            "risk_label": "Low risk",
        }

    # Embed text
    emb = embedder.encode([text])
    emb = np.array(emb)  # ensure numpy array

    # Predict risk
    pred = float(regressor.predict(emb)[0])

    # Clamp to 0–100
    pred = max(0.0, min(100.0, pred))

    # Convert numeric score → label
    if pred < 30:
        status = "Low risk"
    elif pred < 60:
        status = "Moderate risk"
    else:
        status = "High risk"

    return {
        "risk_score": pred,
        "status": status,
        "risk_label": status,
    }
