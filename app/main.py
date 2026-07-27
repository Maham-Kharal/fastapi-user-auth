from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
from app.models import models
from app.routers import auth, user, websocket, chat, eval

# ...further down, next to your other include_router lines...


import logging
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Auth + Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(websocket.router)
app.include_router(chat.router)
app.include_router(eval.router)

from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings

@app.post("/trigger-report")
async def trigger_report():
    redis = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    job = await redis.enqueue_job("generate_and_email_report")
    return {"status": "queued", "job_id": job.job_id}

app.mount("/static", StaticFiles(directory="static"), name="static")