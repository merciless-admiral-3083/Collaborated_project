# backend/ml/train.py
import os
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

BASE = os.path.dirname(__file__)
DATA_CSV = os.path.join(BASE, "..", "data", "dataset.csv")
MODEL_PKL = os.path.join(BASE, "model.pkl")
VECTORIZER_PKL = os.path.join(BASE, "vectorizer.pkl")

def train(save_model=True):
    """
    Train pipeline: TF-IDF (text) -> RandomForestRegressor.
    Expects dataset.csv with columns: 'text' and 'risk_score' (0-100).
    """
    if not os.path.exists(DATA_CSV):
        raise FileNotFoundError(f"Dataset not found at {DATA_CSV}")

    df = pd.read_csv(DATA_CSV).dropna(subset=["risk_score"])

    feature_cols = [
        "news_negative_pct",
        "keyword_score",
        "weather_risk",
        "port_delay_index",
        "supplier_concentration",
        "hist_delay"
    ]

    X = df[feature_cols].values
    y = df["risk_score"].values


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    pipeline = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42
    )


    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    if save_model:
        # Save the whole pipeline as model.pkl (easiest)
        joblib.dump(pipeline, MODEL_PKL)

    metrics = {"mae": mae, "r2": r2, "n_train": len(X_train)}
    print("Training finished:", metrics)
    return pipeline, metrics

if __name__ == "__main__":
    train(save_model=True)
