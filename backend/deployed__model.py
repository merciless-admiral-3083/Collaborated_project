import joblib
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "regressor.pkl")

# Load model only once
try:
    model = joblib.load(MODEL_PATH)
    print("ML Model loaded successfully")
except:
    model = None
    print("⚠️ ML Model NOT FOUND. Train it first using train.py")


def predict_risk(data: dict):
    """
    data = {
        "port_delay": float,
        "political_risk": float,
        "fuel_cost": float,
        "demand_variation": float
    }
    """

    if model is None:
        return {"error": "Model not trained yet."}

    input_vector = np.array([
        data["port_delay"],
        data["political_risk"],
        data["fuel_cost"],
        data["demand_variation"]
    ]).reshape(1, -1)

    prediction = model.predict(input_vector)[0]

    return {"risk_score": float(prediction)}
