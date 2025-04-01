from contextlib import asynccontextmanager

from fastapi import FastAPI
from configs.config import settings
from configs.db import init_db
from routes import router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Connecting to database")
    await init_db()
    print("Connected to database")
    yield

app = FastAPI(title=settings.APP_TITLE, lifespan=life_span)

@app.get("/api/v1/live")
async def live():
    return { "message": True }

app.include_router(router=router, prefix="/api/v1")