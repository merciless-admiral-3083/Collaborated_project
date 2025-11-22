# backend/ml/train_regressor.py
import os
import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, r2_score
DATA_CSV = os.path.join("backend", "data", "training.csv")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"   # fast, small
EMBED_INFO = os.path.join("backend", "ml", "embedder_name.txt")
MODEL_OUT = "backend/ml/regressor.pkl"

def load_data(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "risk_score"])
    df["risk_score"] = df["risk_score"].astype(float)
    return df

def main():
    if not os.path.exists(DATA_CSV):
        raise FileNotFoundError(f"Training CSV not found: {DATA_CSV}. Run collect_training_data.py first.")
    df = load_data(DATA_CSV)
    texts = df["text"].tolist()
    y = df["risk_score"].values

    print(f"Loaded {len(texts)} samples")

    # embed
    embedder = SentenceTransformer(EMBED_MODEL_NAME)
    print("Computing embeddings...")
    X = embedder.encode(texts, show_progress_bar=True, batch_size=64)

    # train/val
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.12, random_state=42)

    # MLP regressor
    reg = MLPRegressor(hidden_layer_sizes=(512,256), max_iter=80, random_state=42)
    print("Training regressor...")
    reg.fit(X_train, y_train)

    preds = reg.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)
    print(f"Validation MAE: {mae:.3f}, R2: {r2:.3f}")

    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(reg, MODEL_OUT)
    with open(EMBED_INFO, "w") as f:
        f.write(EMBED_MODEL_NAME)

    print("Saved regressor:", MODEL_OUT)
    print("Saved embedder info:", EMBED_INFO)

if __name__ == "__main__":
    main()
