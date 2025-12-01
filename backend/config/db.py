# backend/config/db.py
from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)

db = client["risk_prediction"]          # database name
predictions_collection = db["predictions"]  # collection reference
