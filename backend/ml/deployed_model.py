import os
import numpy as np
import joblib
from typing import Dict
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Load Embedder
# -----------------------------
EMBEDDER_NAME_FILE = os.path.join(BASE_DIR, "embedder_name.txt")
MODEL_PKL = os.path.join(BASE_DIR, "regressor.pkl")

embedder = None
regressor = None

# Load embedder name
try:
    with open(EMBEDDER_NAME_FILE, "r") as f:
        EMBEDDER_NAME = f.read().strip()
    embedder = SentenceTransformer(EMBEDDER_NAME)
    print(f"✅ Loaded sentence embedder: {EMBEDDER_NAME}")
except Exception as e:
    print("⚠ Failed to load embedder:", e)
    embedder = None

# Load ML regressor
try:
    regressor = joblib.load(MODEL_PKL)
    print(f"✅ Loaded ML regressor model: {MODEL_PKL}")
except Exception as e:
    print("⚠ Failed to load regressor model:", e)
    regressor = None


# --------------------------------------
#           MAIN PREDICT FUNCTION
# --------------------------------------
def predict_text(text: str) -> Dict:
    """
    Returns:
        {
            "risk_score": float 0–100,
            "status": "Low risk" | "Moderate risk" | "High risk",
            "risk_label": same as status
        }
    """

    # -----------------------------
    # Handle empty text
    # -----------------------------
    if not text or not text.strip():
        return {
            "risk_score": 10.0,
            "status": "Low risk",
            "risk_label": "Low risk",
        }

    # -----------------------------
    # Fallback if model not loaded
    # -----------------------------
    if embedder is None or regressor is None:
        return {
            "risk_score": 20.0,
            "status": "Low risk",
            "risk_label": "Low risk",
        }

    # -----------------------------
    # Embed text
    # -----------------------------
    try:
        emb = embedder.encode([text])
        emb = np.array(emb)
    except Exception as e:
        print("⚠ Embedding failed:", e)
        return {
            "risk_score": 15.0,
            "status": "Low risk",
            "risk_label": "Low risk",
        }

    # -----------------------------
    # Predict using regressor
    # -----------------------------
    try:
        pred = float(regressor.predict(emb)[0])
    except Exception as e:
        print("⚠ Prediction failed:", e)
        return {
            "risk_score": 18.0,
            "status": "Low risk",
            "risk_label": "Low risk",
        }

    # Clamp to 0–100
    pred = max(0.0, min(100.0, pred))

    # Convert numeric → status
    if pred < 30:
        status = "Low risk"
    elif pred < 60:
        status = "Moderate risk"
    else:
        status = "High risk"

    return {
        "risk_score": round(pred, 2),
        "status": status,
        "risk_label": status,
    }
