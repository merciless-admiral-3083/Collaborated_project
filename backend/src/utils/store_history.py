# backend/src/utils/store_history.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("backend", "data", "history.sqlite")

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS risk_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        risk_score REAL,
        ts TEXT
    );
    """)
    conn.commit()
    conn.close()

def store_risk(country: str, risk_score: float):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO risk_history (country, risk_score, ts) VALUES (?, ?, ?)",
                (country, float(risk_score), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_history(country: str, days: int = 30):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT ts, risk_score FROM risk_history WHERE country = ? ORDER BY ts DESC LIMIT ?", (country, days))
    rows = cur.fetchall()
    conn.close()
    return [{"ts": r[0], "risk_score": r[1]} for r in rows]
