from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
from app.models import models
from app.routers import auth, user, websocket

from app.routers import auth, user, websocket, chat   # add chat here

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

app.mount("/static", StaticFiles(directory="static"), name="static")