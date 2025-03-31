import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from configs.config import settings
from configs.db import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Connecting to db")
    await init_db()
    print("Connected to db")
    yield

app = FastAPI(title=settings.APP_TITLE, lifespan=life_span)