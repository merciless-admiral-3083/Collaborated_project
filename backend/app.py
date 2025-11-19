from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.data_ingestion.fetch_news import fetch_news_for_country
from src.ml_models.risk_predictor import compute_risk_from_news
from dotenv import load_dotenv
import os

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
app = FastAPI()

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

@app.post("/api/analyze")
def analyze_data(data: CountryData):
    country = data.country

    # fetch news
    articles = fetch_news_for_country(country, page_size=10)

    print("DEBUG ARTICLES:", articles)  

    risk = compute_risk_from_news(articles)

    return {
        "country": country,
        "risk_score": risk["risk_score"],
        "status": risk["status"],
        "top_risk_factors": risk["top_risk_factors"],
        "top_articles": risk["top_articles"],
    }

@app.get("/api/global_summary")
def get_summary():
    return {
        "total_ports": 120,
        "alerts_active": 8,
        "avg_risk_score": 64.3
    }

@app.get("/api/risk_score/{country}")
def get_risk_score(country: str):
    articles = fetch_news_for_country(country, page_size=5)
    risk = compute_risk_from_news(articles)

    return {
        "country": country,
        "risk_score": risk["risk_score"],
        "status": risk["status"]
    }
