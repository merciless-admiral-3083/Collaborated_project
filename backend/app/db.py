from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
import logging

load_dotenv()

log = logging.getLogger("app.db")
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
log.addHandler(handler)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:root@mongo:27017")
DB_NAME = os.getenv("DB_NAME", "collabdb")

# Lightweight dummy collection to avoid raising in routes when DB is unavailable
class DummyCollection:
    def __init__(self, name):
        self._name = name

    def find(self, *args, **kwargs):
        log.warning("DB unavailable — DummyCollection.find() called for %s", self._name)
        return []

    def aggregate(self, *args, **kwargs):
        log.warning("DB unavailable — DummyCollection.aggregate() called for %s", self._name)
        return []

    def insert_one(self, *args, **kwargs):
        log.warning("DB unavailable — DummyCollection.insert_one() called for %s", self._name)
        class R: inserted_id = None
        return R()

    def update_one(self, *args, **kwargs):
        log.warning("DB unavailable — DummyCollection.update_one() called for %s", self._name)
        class R: matched_count = 0; modified_count = 0
        return R()

# Try to connect
client = None
db = None
orders_collection = shipments_collection = inventory_collection = users_collection = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # force a connection / auth check
    client.admin.command("ping")
    db = client[DB_NAME]
    orders_collection = db["orders"]
    shipments_collection = db["shipments"]
    inventory_collection = db["inventory"]
    users_collection = db["users"]
    log.info("Connected to MongoDB: %s, using DB: %s", MONGO_URI, DB_NAME)
except errors.OperationFailure as e:
    # authentication or authorization error
    log.error("MongoDB authentication failure: %s", e)
    log.error("Check MONGO_URI credentials and authSource in your .env or Docker setup.")
except errors.ServerSelectionTimeoutError as e:
    log.error("MongoDB server selection/connection timeout: %s", e)
except Exception as e:
    log.error("Unexpected error connecting to MongoDB: %s", e)

# If any failure, provide dummy collections so routes don't crash with 500s
if client is None or db is None:
    log.warning("Using dummy collections because MongoDB connection failed.")
    orders_collection = orders_collection or DummyCollection("orders")
    shipments_collection = shipments_collection or DummyCollection("shipments")
    inventory_collection = inventory_collection or DummyCollection("inventory")
    users_collection = users_collection or DummyCollection("users")