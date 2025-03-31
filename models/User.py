# models.py
from beanie import Document

class User(Document):
    email: str
    full_name: str = ""
    hashed_password: str | None = None
    google_id: str | None = None
    picture: str | None = None

    class Settings:
        collection = "users"
