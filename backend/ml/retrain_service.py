# import joblib
# import os
# from datetime import datetime
# from sklearn.ensemble import RandomForestClassifier
# from database import db  # adjust if needed

# MODEL_PATH = "ml/model.pkl"
# MODEL_VERSION_PATH = "ml/model_version.txt"


# def retrain_model():

#     # Fetch historical prediction data
#     records = list(db.predictions.find())

#     if len(records) < 10:
#         return {"error": "Not enough data to retrain"}

#     X = []
#     y = []

#     for r in records:
#         features = r["input_data"]
#         label = r["result"]["risk_level"]

#         X.append(list(features.values()))
#         y.append(label)

#     model = RandomForestClassifier(n_estimators=100)
#     model.fit(X, y)

#     # Save model
#     joblib.dump(model, MODEL_PATH)

#     # Update model version
#     version = datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     with open(MODEL_VERSION_PATH, "w") as f:
#         f.write(version)

#     return {
#         "message": "Model retrained successfully",
#         "new_version": version,
#         "data_used": len(records)
#     }


import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from database import db
from ml.deployed_model import reload_model

MODEL_PATH = "ml/model.pkl"
MODEL_VERSION_PATH = "ml/model_version.txt"


def retrain_model_background():

    retrain_log = {
        "status": "running",
        "started_at": datetime.utcnow(),
    }

    log_id = db.retrain_logs.insert_one(retrain_log).inserted_id

    try:
        records = list(db.predictions.find())

        if len(records) < 10:
            db.retrain_logs.update_one(
                {"_id": log_id},
                {"$set": {"status": "failed", "reason": "Not enough data"}}
            )
            return

        X = []
        y = []

        for r in records:
            X.append(list(r["input_data"].values()))
            y.append(r["result"]["risk_level"])

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)

        joblib.dump(model, MODEL_PATH)

        version = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        with open(MODEL_VERSION_PATH, "w") as f:
            f.write(version)

        reload_model()

        db.retrain_logs.update_one(
            {"_id": log_id},
            {"$set": {
                "status": "completed",
                "completed_at": datetime.utcnow(),
                "model_version": version,
                "data_used": len(records)
            }}
        )

    except Exception as e:
        db.retrain_logs.update_one(
            {"_id": log_id},
            {"$set": {
                "status": "failed",
                "error": str(e)
            }}
        )


def retrain_model():
    # Synchronous wrapper for retrain_model_background
    retrain_model_background()
    return {"message": "Retraining started"}
