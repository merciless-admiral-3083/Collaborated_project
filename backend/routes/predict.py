# from fastapi import APIRouter
# import joblib
# import os

# router = APIRouter()

# MODEL_DIR = "ml"
# MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

# # Load model once when API starts
# try:
#     model = joblib.load(MODEL_PATH)
# except Exception as e:
#     model = None
#     print(f"⚠ Prediction model could not be loaded: {e}")

# @router.post("/predict")
# def predict(payload: dict):
#     if model is None:
#         return {"error": "Model not loaded"}

#     input_features = payload.get("features")

#     if input_features is None:
#         return {"error": "Missing 'features' data"}

#     prediction = model.predict([input_features])[0]
#     return {"prediction": float(prediction)}


# backend/routes/predict.py
from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from config.db import predictions_collection
import joblib, os

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")
model = joblib.load(MODEL_PATH)

class PredictionInput(BaseModel):
    news_negative_pct: float
    keyword_score: float
    weather_risk: float
    port_delay_index: float
    supplier_concentration: float
    hist_delay: float

@router.post("/predict")
async def predict_risk(data: PredictionInput):
    features = [
        data.news_negative_pct,
        data.keyword_score,
        data.weather_risk,
        data.port_delay_index,
        data.supplier_concentration,
        data.hist_delay,
    ]
    prediction = float(model.predict([features])[0])

    # Save to MongoDB (this will auto-create DB & collection if not exists)
    record = {
        "input_features": data.dict(),
        "prediction": prediction,
        "timestamp": datetime.utcnow()
    }
    inserted = predictions_collection.insert_one(record)

    return {"prediction": prediction, "id": str(inserted.inserted_id)}
