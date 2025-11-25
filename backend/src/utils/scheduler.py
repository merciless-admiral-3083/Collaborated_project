# backend/src/utils/scheduler.py
import os
import logging
import requests
import traceback
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from typing import List

from src.data_ingestion.fetch_news import fetch_news_for_country
from src.ml_models.risk_predictor import compute_risk_from_news
from src.utils.store_history import store_risk

_scheduler = None

log = logging.getLogger("scheduler")
log.setLevel(logging.INFO)

# Try to import deployed ML model (optional)
try:
    from ml.deployed_model import predict_text as ml_predict
    HAS_ML = True
    log.info("Deployed ML model found for scheduler.")
except Exception:
    ml_predict = None
    HAS_ML = False
    log.info("No deployed ML model found; scheduler will use heuristic fallback.")

# Default country list - you may edit or read from a file
DEFAULT_COUNTRIES = [
    "India", "United States", "China", "Germany", "United Kingdom",
    "France", "Japan", "Brazil", "Australia", "Russia",
    "Canada", "South Africa", "Italy", "Spain", "Mexico"
]

scheduler = BackgroundScheduler()
_job = None

def _collect_and_store(country: str):
    try:
        log.info(f"Scheduler: fetching news for {country}")
        articles = fetch_news_for_country(country, page_size=12)

        combined = "\n".join(((a.get("title") or "") + " " + (a.get("description") or "")) for a in articles)

        if HAS_ML:
            try:
                pred = ml_predict(combined)
                score = float(pred.get("risk_score", 0))
                status = pred.get("status") or pred.get("risk_label") or "Model"
                explanation = pred.get("explanation", "")
            except Exception as e:
                log.exception("Scheduler ML predict failed, falling back to heuristic: %s", e)
                heuristic = compute_risk_from_news(articles)
                score = heuristic.get("risk_score", 10)
                status = heuristic.get("status", "Low risk")
                explanation = heuristic.get("explanation", "")
        else:
            heuristic = compute_risk_from_news(articles)
            score = heuristic.get("risk_score", 10)
            status = heuristic.get("status", "Low risk")
            explanation = heuristic.get("explanation", "")

        # store numeric value to history DB
        try:
            store_risk(country, float(score))
        except Exception as e:
            log.exception("Failed to store risk in DB for %s: %s", country, e)

        log.info(f"Stored {country} risk={score} ({status}) at {datetime.utcnow().isoformat()}")
    except Exception as e:
        log.exception("Scheduler: unexpected error for %s: %s", country, e)


def run_once_for_all(countries: List[str] = None):
    countries = countries or DEFAULT_COUNTRIES
    for c in countries:
        _collect_and_store(c)


def schedule_periodic(interval_minutes: int = 360, countries: List[str] = None):
    """Start periodic job to fetch data. interval_minutes default = 360 (6 hours)."""
    global _job
    countries = countries or DEFAULT_COUNTRIES
    if _job:
        scheduler.remove_job(_job.id)
    # Add a job that runs every interval_minutes
    _job = scheduler.add_job(lambda: run_once_for_all(countries),
                             'interval',
                             minutes=interval_minutes,
                             next_run_time=datetime.utcnow())  # start immediately
    log.info("Scheduler started: interval %s minutes, countries: %s", interval_minutes, countries)

def _global_scan_job():
    """
    This job cycles through a predefined list of countries (or your DB list)
    and calls the analyze endpoint to compute & store risk.
    """
    try:
        # You can expand this list or load from DB
        countries = ["India", "United States", "China", "Germany", "Brazil"]
        for c in countries:
            try:
                resp = requests.post("http://127.0.0.1:8000/api/analyze", json={"country": c}, timeout=30)
                if resp.ok:
                    print("Scanned:", c, resp.json().get("risk_score"))
                else:
                    print("Scan failed for", c, resp.text)
            except Exception as e:
                print("Error scanning", c, e)
    except Exception:
        traceback.print_exc()

def start_scheduler(interval_minutes: int = 360):
    global _scheduler
    if _scheduler is not None:
        print("Scheduler already running.")
        return _scheduler

    _scheduler = BackgroundScheduler()
    _scheduler.start()
    # run job every `interval_minutes`
    _scheduler.add_job(_global_scan_job, trigger=IntervalTrigger(minutes=interval_minutes), id="global_scan", replace_existing=True)
    atexit.register(lambda: _scheduler.shutdown(wait=False))
    print(f"Scheduler started: interval={interval_minutes}m")
    return _scheduler

def stop_scheduler():
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        print("Scheduler stopped.")
        
def run_once_for_all():
    _global_scan_job()