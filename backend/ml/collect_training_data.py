# backend/ml/collect_training_data.py
import csv
import os
from datetime import datetime
from src.data_ingestion.fetch_news import fetch_news_for_country
from src.ml_models.risk_predictor import compute_risk_from_news

OUT_CSV = os.path.join("backend", "data", "training.csv")

# countries to bootstrap — extend as needed
COUNTRIES = [
    "India", "United States", "China", "Germany", "United Kingdom",
    "France", "Japan", "Brazil", "Australia", "Russia"
]

def collect_one_run():
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    rows = []
    for country in COUNTRIES:
        articles = fetch_news_for_country(country, page_size=20)
        combined_text = "\n".join(((a.get("title") or "") + " " + (a.get("description") or "")) for a in articles)
        risk = compute_risk_from_news(articles)
        rows.append({
            "country": country,
            "date": datetime.utcnow().isoformat(),
            "text": combined_text,
            "risk_score": risk["risk_score"]
        })
        print(f"Collected {len(articles)} articles for {country} -> score {risk['risk_score']}")

    write_headers = not os.path.exists(OUT_CSV)
    with open(OUT_CSV, "a", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        if write_headers:
            writer.writerow(["country", "date", "text", "risk_score"])
        for r in rows:
            writer.writerow([r["country"], r["date"], r["text"], r["risk_score"]])

if __name__ == "__main__":
    collect_one_run()
    print("Data appended to", OUT_CSV)
