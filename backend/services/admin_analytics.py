from database import db
from datetime import datetime, timedelta

def get_admin_stats():

    total_users = db.users.count_documents({})
    total_predictions = db.predictions.count_documents({})

    risk_distribution = list(
        db.predictions.aggregate([
            {
                "$group": {
                    "_id": "$result.risk_level",
                    "count": {"$sum": 1}
                }
            }
        ])
    )

    last_7_days = datetime.utcnow() - timedelta(days=7)

    predictions_last_7_days = db.predictions.count_documents({
        "created_at": {"$gte": last_7_days}
    })

    latest_retrain = db.retrain_logs.find_one(
        {},
        sort=[("started_at", -1)]
    )

    if latest_retrain:
        latest_retrain["_id"] = str(latest_retrain["_id"])

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "risk_distribution": risk_distribution,
        "predictions_last_7_days": predictions_last_7_days,
        "latest_retrain": latest_retrain
    }