import os

class Settings:
    SECRET_KEY: str = "3991ff6de703a5f502c5d35ad366a7491d08e3e12cc06742669897f39377f434"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "collabdb")

settings = Settings()
