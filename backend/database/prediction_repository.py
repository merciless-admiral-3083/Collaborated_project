from datetime import datetime
from database.mongo import db

predictions_collection = db["predictions"]

async def save_prediction(user_id: str, input_data: dict, result: dict):
    document = {
        "user_id": user_id,
        "input": input_data,
        "result": result,
        "created_at": datetime.utcnow()
    }
    await predictions_collection.insert_one(document)