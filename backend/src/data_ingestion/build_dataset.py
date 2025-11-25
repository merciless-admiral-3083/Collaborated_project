"""
backend/src/data_ingestion/build_dataset.py

ETL script to build a dataset for supply-chain disruption risk prediction.

Outputs:
  backend/data/dataset.csv

Usage examples:
  # basic: build dataset for default countries
  python backend/src/data_ingestion/build_dataset.py

  # specify countries and output file
  python backend/src/data_ingestion/build_dataset.py --countries IN,US,CN --out ../data/dataset.csv --pagesize 10

Notes:
- Relies on your fetch_news_for_country() and compute_risk_from_news() helpers.
- If external APIs (weather, port) are not configured, the script uses safe mock values.
"""
import os
import argparse
import time
import csv
import random
from typing import List, Dict, Any

# Import existing project helpers
try:
    from src.data_ingestion.fetch_news import fetch_news_for_country
    from src.ml_models.risk_predictor import compute_risk_from_news
except Exception:
    # fallback for alternative import path if running from different cwd
    from src.data_ingestion.fetch_news import fetch_news_for_country
    from src.ml_models.risk_predictor import compute_risk_from_news

# light NLP helper
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except Exception:
    TEXTBLOB_AVAILABLE = False

# Optional: OpenWeatherMap (if you add key to .env)
import os
OWM_KEY = os.getenv("OPENWEATHER_KEY", "") or os.getenv("OPENWEATHERMAP_KEY", "")

# Optional: marine/port APIs - mocked by default
MARINETRAFFIC_KEY = os.getenv("MARINETRAFFIC_KEY", "")

OUT_DIR_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
OUT_DIR_DEFAULT = os.path.normpath(OUT_DIR_DEFAULT)
DEFAULT_OUT = os.path.join(OUT_DIR_DEFAULT, "dataset.csv")


# --- helpers ---------------------------------------------------------------
def extract_text_features(articles: List[Dict[str, Any]]):
    """
    Given list of article dicts (title, description, source), return:
      - news_negative_pct: estimated negative polarity percentage (0-100)
      - keyword_score: integer keyword-based score
      - top_headlines: concatenated text
    """
    combined_texts = []
    for a in articles:
        t = (a.get("title") or "") + " " + (a.get("description") or "")
        combined_texts.append(t.strip())

    bigtext = " ".join(combined_texts)
    # sentiment (TextBlob) fallback to small negative default if not installed
    if TEXTBLOB_AVAILABLE and bigtext.strip():
        try:
            polarity = TextBlob(bigtext).sentiment.polarity  # -1..1
            news_negative_pct = max(0.0, -polarity * 100)  # convert negative polarity to percent
        except Exception:
            news_negative_pct = 10.0
    else:
        # heuristic fallback: if keywords present, increase negativity
        news_negative_pct = 10.0

    # keyword list and scoring (matches your risk keywords)
    keywords = [
        "strike", "delay", "congestion", "shortage", "conflict",
        "sanction", "flood", "earthquake", "shutdown", "protest", "blockade", "virus", "pandemic"
    ]
    kw_score = 0
    text_lower = bigtext.lower()
    for kw in keywords:
        if kw in text_lower:
            kw_score += 10

    return {
        "news_negative_pct": round(float(news_negative_pct), 3),
        "keyword_score": int(kw_score),
        "combined_text": bigtext[:10000]  # store truncated text for debug if needed
    }


def fetch_weather_risk(country: str):
    """
    Simple weather-risk stub. If OpenWeatherMap key provided, you can add a real call.
    Returns an integer-like weather risk score (0,5,10,20).
    """
    if OWM_KEY:
        # TODO: call OpenWeatherMap by city/country -> compute severity
        # Keep lightweight placeholder to avoid external deps here.
        return random.choice([0, 5, 10, 20])
    return random.choice([0, 0, 0, 5, 10])  # default low probability


def fetch_port_delay_index(country: str):
    """
    Port delay index stub. If MARINETRAFFIC_KEY available, implement live retrieval.
    Returns a 0-100 index.
    """
    if MARINETRAFFIC_KEY:
        # TODO: implement marine traffic calls
        return random.uniform(0, 100)
    # General heuristic: larger economies might have higher activity hence slightly larger index
    base = 10.0
    if country.upper() in ("CN", "US", "IN", "DE"):
        base = 15.0
    return round(max(0, random.gauss(base, 12)), 3)


def build_row_for_country(country: str, page_size: int = 10):
    """
    Build one aggregated row for the given country:
    - fetch recent news
    - compute text features
    - fetch simple external signals or fallback
    - compute label using compute_risk_from_news(articles) heuristic
    """
    articles = fetch_news_for_country(country, page_size=page_size)
    if articles is None:
        articles = []

    text_feats = extract_text_features(articles)
    weather_risk = fetch_weather_risk(country)
    port_delay_index = fetch_port_delay_index(country)
    # supplier concentration is a placeholder (0-1)
    supplier_concentration = round(random.random(), 3)

    # hist_delay: we can use recent port_delay_index as historical approx
    hist_delay = round(max(0, port_delay_index * random.uniform(0.6, 1.2)), 3)

    # use your heuristic to create the weak-supervised label
    heuristic = compute_risk_from_news(articles) if len(articles) > 0 else {"risk_score": 10.0}
    label = float(heuristic.get("risk_score", 10.0))

    row = {
        "country": country,
        "news_negative_pct": text_feats["news_negative_pct"],
        "keyword_score": text_feats["keyword_score"],
        "weather_risk": weather_risk,
        "port_delay_index": port_delay_index,
        "supplier_concentration": supplier_concentration,
        "hist_delay": hist_delay,
        "risk_score": round(label, 3),
        "n_articles": len(articles),
        "sample_headlines": (text_feats["combined_text"][:500]).replace("\n", " ")
    }
    return row


# --- main ETL flow ---------------------------------------------------------
def build_dataset(countries: List[str], pagesize: int = 10, out_path: str = DEFAULT_OUT, pause_seconds: float = 1.0):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fieldnames = [
        "ts", "country", "news_negative_pct", "keyword_score", "weather_risk",
        "port_delay_index", "supplier_concentration", "hist_delay", "risk_score",
        "n_articles", "sample_headlines"
    ]
    # append mode support: if file exists, we will append new rows
    append = os.path.exists(out_path)
    mode = "a" if append else "w"
    written = 0
    with open(out_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not append:
            writer.writeheader()

        for c in countries:
            try:
                row = build_row_for_country(c, page_size=pagesize)
                row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                # ensure all fields present
                writer.writerow({k: row.get(k, "") for k in fieldnames})
                written += 1
                print(f"[+] written row for {c}: risk={row['risk_score']}, n_articles={row['n_articles']}")
            except Exception as e:
                print(f"[!] failed for {c}: {e}")
            time.sleep(pause_seconds)

    print(f"Dataset build complete. {written} rows written to {out_path}")
    return out_path


# --- CLI ------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Build dataset CSV for supply-chain risk model.")
    p.add_argument("--countries", type=str, default="IN,US,CN,DE,BR,SG,MX,NL,KR,JP",
                   help="Comma-separated list of country codes (ISO2 or custom names).")
    p.add_argument("--pagesize", type=int, default=8, help="How many news articles to fetch per country.")
    p.add_argument("--out", type=str, default=DEFAULT_OUT, help="Output CSV path.")
    p.add_argument("--pause", type=float, default=1.0, help="Seconds to pause between API calls to avoid rate limits.")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    countries = [c.strip() for c in args.countries.split(",") if c.strip()]
    out = os.path.abspath(args.out)
    print("Building dataset for countries:", countries)
    print("Saving to:", out)
    build_dataset(countries, pagesize=args.pagesize, out_path=out, pause_seconds=args.pause)
