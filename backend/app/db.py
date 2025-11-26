from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:root@mongo:27017")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["collabdb"]

# Optional: define collections here
orders_collection = db["orders"]
shipments_collection = db["shipments"]
inventory_collection = db["inventory"]
users_collection = db["users"]
