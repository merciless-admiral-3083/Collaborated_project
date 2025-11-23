from fastapi import APIRouter
from backend.app.db import client
from datetime import datetime

router = APIRouter()

@router.get("/global_summary")
def global_summary():
    db = client["country_risk"]
    collection = db["history"]

    pipeline = [
        {
            "$sort": {"ts": -1}
        },
        {
            "$group": {
                "_id": "$country",
                "latest_risk": {"$first": "$risk_score"},
                "latest_time": {"$first": "$ts"},
            }
        }
    ]

    rows = list(collection.aggregate(pipeline))

    country_risk_map = {
        row["_id"]: row["latest_risk"]
        for row in rows
    }

    return {
        "timestamp": datetime.utcnow(),
        "country_risk_map": country_risk_map
    }
