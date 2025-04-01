# models.py
from beanie import Document
from datetime import datetime

class User(Document):
    email: str
    full_name: str = ""
    hashed_password: str | None = None
    google_id: str | None = None
    picture: str | None = None
    created_at: datetime = datetime.utcnow()
    update_now: datetime = datetime.utcnow()

    class Settings:
        collection = "users"

    @property
    def id(self):
        return str(self._id)