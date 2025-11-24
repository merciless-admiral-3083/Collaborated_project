from fastapi import APIRouter
from app.db import client

router = APIRouter()

@router.get("/history/{country}")
def get_history(country: str, days: int = 30):
    db = client["country_risk"]
    col = db["history"]

    docs = col.find({"country": country}).sort("ts", -1).limit(days)

    return [
        {
            "ts": d["ts"],
            "risk_score": d.get("risk_score", 0)
        }
        for d in docs
    ]
