import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
PORT = os.getenv("PORT", 8000)
