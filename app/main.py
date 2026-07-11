from fastapi import FastAPI

from app.core.database import engine, Base
from app import models
from app.routers import auth, user

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Auth API")

app.include_router(auth.router)
app.include_router(user.router)