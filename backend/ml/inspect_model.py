import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("\n=== MODEL LOADED SUCCESSFULLY ===")

    # RandomForestRegressor has no feature names inside the model itself.
    # But if your training code saved metadata, load that instead.
    metadata_path = os.path.join(os.path.dirname(__file__), "training_metadata.pkl")

    if os.path.exists(metadata_path):
        metadata = joblib.load(metadata_path)
        feature_cols = metadata.get("feature_cols")
        print("\nFeature Columns (from metadata):")
        print(feature_cols)
    else:
        print("\n⚠ No metadata found. Using fallback:")
        print("The model itself does NOT store feature names for RandomForestRegressor.")

except Exception as e:
    print("Error loading model:", e)
