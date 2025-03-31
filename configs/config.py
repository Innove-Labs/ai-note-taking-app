# config.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    MONGO_URI = os.getenv("MONGO_URI")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60 * 24 * 3
    APP_TITLE = os.getenv("APP_TITLE") or "APP"
settings = Settings()
