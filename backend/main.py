from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import joblib
import numpy as np

# -----------------------------
# INTERNAL IMPORTS
# -----------------------------
from src.data_ingestion.fetch_news import fetch_news_for_country
from src.ml_models.risk_predictor import compute_risk_from_news
from src.utils.store_history import store_risk, init_db
from src.utils.scheduler import start_scheduler, stop_scheduler

# Routers
from app.routes.history import router as history_router
from app.routes.global_summary import router as global_summary_router
from app.routes.orders import router as orders_router
from app.routes.shipments import router as shipments_router
from app.routes.inventory import router as inventory_router
from app.routes.auth import router as auth_router

# ML training + predictor functions
from ml.train import train as train_model
from deployed_model import predict_text, predict_from_features

# -----------------------------
# ENV + APP INIT
# -----------------------------
load_dotenv()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders_router, prefix="/api")
app.include_router(shipments_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(global_summary_router, prefix="/api")
import os

# -----------------------------
# MODEL LOADING (robust)
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.pkl")
model = None
model_loaded = False

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
    print(f"✅ Loaded pipeline model: {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"⚠ Model load failed ({MODEL_PATH}):", e)



# Model is usable if it loaded; vectorizer is optional.
HAS_DEPLOYED_MODEL = model_loaded
if not HAS_DEPLOYED_MODEL:
    print("⚠ No model available. Will try embedder regressor or heuristic.")

# -----------------------------
# BASIC TEST ROUTE
# -----------------------------
@app.get("/api/hello")
def root():
    return {"message": "Backend connected successfully 🚀"}

# -----------------------------
# ANALYZE ROUTE
# -----------------------------
class CountryData(BaseModel):
    country: str

@app.post("/api/analyze")
def analyze_data(data: CountryData):
    country = data.country
    articles = fetch_news_for_country(country, page_size=12)

    combined = "\n".join(
        (a.get("title") or "") + " " + (a.get("description") or "")
        for a in articles
    )

    # AI MODEL PREDICTION - use feature-based model if available
    if HAS_DEPLOYED_MODEL and model is not None:
        try:
            # Extract heuristic summary (explanation + top articles) and compute features
            heuristic = compute_risk_from_news(articles)

            # Compute simple text-derived features: negative sentiment pct and keyword score.
            try:
                from textblob import TextBlob
            except Exception:
                TextBlob = None

            # sentiment -> negative pct
            try:
                if TextBlob is not None:
                    # combine title+description for sentiment
                    text_for_sentiment = "\n".join((a.get("title") or "") + " " + (a.get("description") or "") for a in articles)
                    sentiment = TextBlob(text_for_sentiment).sentiment.polarity
                    news_negative_pct = max(0.0, -sentiment * 100)
                else:
                    news_negative_pct = 10.0
            except Exception:
                news_negative_pct = 10.0

            # keyword score (simple count * weight)
            kw_list = ["strike","delay","congestion","shortage","conflict","sanction","flood","earthquake","shutdown","protest","blockade","war","policy","inflation"]
            kw_score = 0
            combined_lower = combined.lower()
            for kw in kw_list:
                if kw in combined_lower:
                    kw_score += 10

            # other features: use reasonable defaults or lookups when available
            weather_risk = 0
            port_delay_index = 5
            supplier_concentration = 0.3
            hist_delay = 5

            X = [[
                news_negative_pct,
                kw_score,
                weather_risk,
                port_delay_index,
                supplier_concentration,
                hist_delay,
            ]]
            
            risk_score = float(model.predict(X)[0])
            risk_score = max(0.0, min(100.0, risk_score))  # Clamp to 0-100

            response = {
                "country": country,
                "risk_score": round(risk_score, 2),
                "status": "AI Model (feature-based)",
                "risk_label": heuristic.get("status"),
                "explanation": heuristic.get("explanation", ""),
                "top_risk_factors": heuristic.get("top_risk_factors", []),
                "top_articles": heuristic.get("top_articles", []),
            }

            store_risk(country, response["risk_score"])
            return response

        except Exception as e:
            print("⚠ Model prediction error:", e)

    

    # FALLBACK HEURISTIC
    risk = compute_risk_from_news(articles)
    try:
        store_risk(country, risk["risk_score"])
    except:
        pass

    return {
        "country": country,
        "risk_score": risk["risk_score"],
        "status": risk["status"],
        "risk_label": risk["status"],
        "explanation": "Heuristic-based explanation.",
        "top_risk_factors": risk["top_risk_factors"],
        "top_articles": risk["top_articles"],
    }

# -----------------------------
# RISK SCORE (simple)
# -----------------------------
@app.get("/api/risk_score/{country}")
def get_risk_score(country: str):
    articles = fetch_news_for_country(country, page_size=5)
    risk = compute_risk_from_news(articles)
    return {
        "country": country,
        "risk_score": risk.get("risk_score"),
        "status": risk.get("status"),
    }

# -----------------------------
# STARTUP / SHUTDOWN TASKS
# -----------------------------
@app.on_event("startup")
def on_startup():
    init_db()
    try:
        start_scheduler(interval_minutes=360)
    except Exception as e:
        print("Scheduler error:", e)

@app.on_event("shutdown")
def on_shutdown():
    try:
        stop_scheduler()
    except:
        pass

# -----------------------------
# TRAIN MODEL
# -----------------------------
@app.post("/api/train")
def api_train(background: bool = True, background_tasks: BackgroundTasks = None):
    if background and background_tasks:
        background_tasks.add_task(train_model, True)
        return {"status": "training_started_background"}

    model, metrics = train_model(save_model=True)
    return {"status": "trained", "metrics": metrics}

# -----------------------------
# PREDICT ENDPOINT
# -----------------------------
class PredictRequest(BaseModel):
    country: str | None = None
    text: str | None = None
    features: dict | None = None

@app.post("/api/predict")
def api_predict(req: PredictRequest):
    try:
        if req.features:
            out = predict_from_features(req.features)
        else:
            combined = (req.text or "") + (" " + req.country if req.country else "")
            out = predict_text(combined, extras={})

        try:
            store_risk(req.country or "UNKNOWN", out["risk_score"])
        except:
            pass

        return out

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/predict")
def predict(data: dict):
    features = data["features"]
    pred = model.predict([features])[0]
    return {"prediction": float(pred)}



@app.get("/api/predict")
async def predict_get():
    return {"message": "This endpoint only accepts POST with data"}


# -----------------------------
# USER AUTH ROUTES
# -----------------------------
class RegisterModel(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


@app.post("/login")
def login_user(user: UserLogin):
    # Here you can add DB/auth logic
    return {"message": "Login successful", "email": user.email}

@app.get("/test")
def test():
    return {"message": "Backend connected successfully!"}

from routes.predict import router as predict_router
app.include_router(predict_router, prefix="/api")



# # main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ------------------- CORS -------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # frontend dev URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # -------------------------------------------

# # Example route
# @app.get("/hello")
# async def hello():
#     return {"message": "Hello from FastAPI!"}
