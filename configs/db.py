from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User

from configs.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_database()
    await init_beanie(database=db, document_models=[User])