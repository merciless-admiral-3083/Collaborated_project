
# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.src.data_ingestion.fetch_news import fetch_news_for_country
from backend.src.ml_models.risk_predictor import compute_risk_from_news
from backend.src.utils.store_history import init_db
from backend.src.utils.store_history import store_risk
from dotenv import load_dotenv
from backend.src.utils.scheduler import start_scheduler, stop_scheduler, run_once_for_all

import os


load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
app = FastAPI()

# ROUTERS (import AFTER app is created)
from backend.app.routes.history import router as history_router
from backend.app.routes.global_summary import router as global_summary_router

app.include_router(history_router, prefix="/api")
app.include_router(global_summary_router, prefix="/api")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CountryData(BaseModel):
    country: str

@app.get("/api/hello")
def read_root():
    return {"message": "Backend connected successfully 🚀"}

# inside backend/app.py — replace analyze_data route with the following

# optional model server
try:
    from backend.ml.deployed_model import predict_text as deployed_predict
    HAS_DEPLOYED_MODEL = True
except Exception:
    HAS_DEPLOYED_MODEL = False

@app.post("/api/analyze")
def analyze_data(data: CountryData):
    country = data.country
    articles = fetch_news_for_country(country, page_size=12)
    # prepare combined text for ML model
    combined = "\n".join(((a.get("title") or "") + " " + (a.get("description") or "")) for a in articles)

    # try deployed learned model
    if HAS_DEPLOYED_MODEL:
        try:
            ml_out = deployed_predict(combined)
            # preserve top_articles & top_factors from heuristic for explainability
            heuristic = compute_risk_from_news(articles)
            response = {
                "country": country,
                "risk_score": round(ml_out["risk_score"], 2),
                "status": ml_out.get("status"),
                "risk_label": ml_out.get("risk_label"),
                "explanation": heuristic.get("explanation", "Model-based prediction."),
                "top_risk_factors": heuristic.get("top_risk_factors", []),
                "top_articles": heuristic.get("top_articles", []),
            }
            # store to DB history (optional) - see DB section below
            try:
                from backend.src.utils.store_history import store_risk  # we'll add this helper
                store_risk(country, response["risk_score"])
            except Exception:
                pass
            return response
        except Exception as e:
            print("Deployed model failed:", e)
            # fallback to heuristic

    # fallback heuristic
    risk = compute_risk_from_news(articles)
    # store to DB if possible
    try:
        from backend.src.utils.store_history import store_risk
        store_risk(country, risk["risk_score"])
    except Exception:
        pass

    return {
        "country": country,
        "risk_score": risk["risk_score"],
        "status": risk["status"],
        "risk_label": risk.get("status"),   # keep compatibility
        "explanation": "Heuristic-based explanation.",
        "top_risk_factors": risk["top_risk_factors"],
        "top_articles": risk["top_articles"],
    }



@app.get("/api/risk_score/{country}")
def get_risk_score(country: str):
    articles = fetch_news_for_country(country, page_size=5)
    risk = compute_risk_from_news(articles)
    return {
        "country": country,
        "risk_score": risk.get("risk_score"),
        "status": risk.get("status"),
    }
# start scheduler on app startup
@app.on_event("startup")
def _on_startup():
    # start periodic job every 6 hours (360 minutes)
    try:
        start_scheduler(interval_minutes=360)
    except Exception as e:
        print("Scheduler start failed:", e)

# stop scheduler on shutdown
@app.on_event("shutdown")
def _on_shutdown():
    try:
        stop_scheduler()
    except Exception:
        pass

