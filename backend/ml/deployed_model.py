import os
import json
import joblib
import numpy as np

import os

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_VERSION = "v1"

MODEL_PATH = os.path.join(MODEL_DIR, f"risk_model_{MODEL_VERSION}.pkl")
FEATURE_IMPORTANCE_PATH = os.path.join(
    MODEL_DIR, f"feature_importance_{MODEL_VERSION}.json"
)
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, "feature_names.json")


class RiskModel:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

        with open(FEATURE_IMPORTANCE_PATH, "r") as f:
            self.feature_importance = json.load(f)

        with open(FEATURE_NAMES_PATH, "r") as f:
            self.feature_names = json.load(f)

    def predict(self, input_data: dict):
        # Ensure correct feature order
        features = np.array(
            [[input_data[feature] for feature in self.feature_names]]
        )

        probability = self.model.predict_proba(features)[0][1]

        risk_level = self._map_risk_level(probability)

        top_drivers = self._get_top_drivers(input_data)

        return {
            "model_version": MODEL_VERSION,
            "risk_probability": float(probability),
            "risk_level": risk_level,
            "top_risk_drivers": top_drivers,
        }

    def _map_risk_level(self, probability):
        if probability < 0.3:
            return "Low"
        elif probability < 0.6:
            return "Medium"
        else:
            return "High"

    def _get_top_drivers(self, input_data):
        # Multiply feature value by importance to estimate contribution
        contributions = {
            feature: input_data[feature] * self.feature_importance[feature]
            for feature in self.feature_names
        }

        # Sort descending
        sorted_features = sorted(
            contributions.items(), key=lambda x: x[1], reverse=True
        )

        return [feature for feature, _ in sorted_features[:3]]