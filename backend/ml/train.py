# backend/ml/train.py
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json

BASE = os.path.dirname(os.path.dirname(__file__))  # backend/ml -> backend
DATA_PATH = os.path.join(BASE, "data", "dataset.csv")
MODEL_OUT = os.path.join(BASE, "ml", "regressor.pkl")
METRICS_OUT = os.path.join(BASE, "ml", "metrics.json")

def generate_mock_dataset(path, n=2000):
    """Generate a synthetic dataset quickly (if real data missing)."""
    import random
    import pandas as pd
    rows = []
    for i in range(n):
        # features that approximate the system
        news_negative = np.clip(np.random.beta(2,6)*100, 0, 100) # negative sentiment %
        keyword_score = np.random.poisson(2) * 5
        weather_risk = np.random.choice([0,5,10,20], p=[0.7,0.15,0.1,0.05])
        port_delay_index = np.clip(np.random.normal(10,8), 0, 100)
        supplier_concentration = np.random.rand()  # 0-1
        # historical delay mean (last 7 days)
        hist_delay = np.clip(np.random.normal(12,10), 0, 100)
        # target roughly correlated
        risk = np.clip(0.4*news_negative + 0.3*keyword_score + 0.2*port_delay_index + 0.2*weather_risk + hist_delay*0.1 + np.random.normal(0,8), 0, 100)
        rows.append({
            "news_negative_pct": news_negative,
            "keyword_score": keyword_score,
            "weather_risk": weather_risk,
            "port_delay_index": port_delay_index,
            "supplier_concentration": supplier_concentration,
            "hist_delay": hist_delay,
            "risk_score": risk
        })
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print("Mock dataset created:", path)

def load_data(path):
    if not os.path.exists(path):
        print("Dataset not found, generating mock dataset.")
        generate_mock_dataset(path)
    df = pd.read_csv(path)
    return df

def train(save_model=True):
    df = load_data(DATA_PATH)
    # features / target
    X = df.drop(columns=["risk_score"])
    y = df["risk_score"]
    # simple split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15, random_state=42)
    # model
    model = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    # eval
    preds = model.predict(X_val)
    mse = mean_squared_error(y_val, preds)
    r2 = r2_score(y_val, preds)
    metrics = {"mse": float(mse), "r2": float(r2)}
    print("Validation metrics:", metrics)
    if save_model:
        os.makedirs(os.path.join(BASE, "ml"), exist_ok=True)
        joblib.dump(model, MODEL_OUT)
        with open(METRICS_OUT, "w") as f:
            json.dump(metrics, f)
        print("Model saved to", MODEL_OUT)
    return model, metrics

if __name__ == "__main__":
    train()
