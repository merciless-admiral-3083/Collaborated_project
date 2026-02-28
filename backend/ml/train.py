import os
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
)

# ---------------------------
# CONFIG
# ---------------------------

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

RANDOM_STATE = 42
N_SAMPLES = 10000


# ---------------------------
# 1️⃣ Generate Domain-Based Dataset
# ---------------------------

def generate_supply_chain_dataset(n_samples=10000):
    np.random.seed(RANDOM_STATE)

    data = pd.DataFrame({
        "political_stability_index": np.random.beta(2, 2, n_samples),
        "logistics_performance_index": np.random.beta(2, 2, n_samples),
        "supplier_financial_health": np.random.beta(2, 2, n_samples),
        "disaster_exposure_score": np.random.beta(2, 5, n_samples),
        "trade_dependency_ratio": np.random.beta(2, 3, n_samples),
        "historical_disruption_rate": np.random.beta(2, 4, n_samples),
        "esg_risk_score": np.random.beta(2, 3, n_samples),
    })

    # Define risk logic (composite weighted formula)
    risk_score = (
        (1 - data["political_stability_index"]) * 0.2 +
        (1 - data["supplier_financial_health"]) * 0.2 +
        data["disaster_exposure_score"] * 0.2 +
        data["historical_disruption_rate"] * 0.2 +
        data["trade_dependency_ratio"] * 0.1 +
        data["esg_risk_score"] * 0.1
    )

    # Binary target
    data["risk_label"] = (risk_score > 0.5).astype(int)

    return data


# ---------------------------
# 2️⃣ Train Model
# ---------------------------

def train():
    print("Generating dataset...")
    df = generate_supply_chain_dataset(N_SAMPLES)

    X = df.drop("risk_label", axis=1)
    y = df["risk_label"]

    feature_names = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    print("Training RandomForest model...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=RANDOM_STATE
    )

    model.fit(X_train, y_train)

    # ---------------------------
    # 3️⃣ Evaluate
    # ---------------------------

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    metrics = {
        "accuracy": float(accuracy),
        "roc_auc": float(roc_auc),
        "classification_report": classification_report(
            y_test, y_pred, output_dict=True
        ),
    }

    print("Accuracy:", accuracy)
    print("ROC-AUC:", roc_auc)

    # ---------------------------
    # 4️⃣ Save Artifacts
    # ---------------------------

    joblib.dump(model, os.path.join(MODEL_DIR, "risk_model_v1.pkl"))

    with open(os.path.join(MODEL_DIR, "metrics_v1.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    with open(os.path.join(MODEL_DIR, "feature_names.json"), "w") as f:
        json.dump(feature_names, f, indent=4)

    feature_importance = dict(
        zip(feature_names, model.feature_importances_)
    )

    with open(os.path.join(MODEL_DIR, "feature_importance_v1.json"), "w") as f:
        json.dump(feature_importance, f, indent=4)

    print("Model and artifacts saved in /models directory.")


if __name__ == "__main__":
    train()