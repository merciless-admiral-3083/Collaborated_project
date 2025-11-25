# backend/src/utils/store_history.py
import sqlite3
import os
from datetime import datetime, timezone
from app.db import client

DB_PATH = os.path.join("backend", "data", "history.sqlite")
DB_NAME = "country_risk"

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    # triggers client import, used earlier - keep as no-op as client is global
    try:
        client.server_info()
    except Exception as e:
        print("Warning: MongoDB not reachable:", e)

def store_risk(country: str, risk_score: float):
    db = client[DB_NAME]
    col = db["history"]
    col.insert_one({
        "country": country,
        "risk_score": float(risk_score),
        "ts": datetime.now(timezone.utc).isoformat()
    })

def get_history(country: str, days: int = 30):
    db = client[DB_NAME]
    col = db["history"]
    docs = col.find({"country": country}).sort("ts", -1).limit(days)
    return [{"ts": d["ts"], "risk_score": d.get("risk_score", 0)} for d in docs]
