from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.models import User
from app.schemas import schemas
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(User.username == user.username, User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.TokenResponse)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        or_(
            User.username == credentials.username_or_email,
            User.email == credentials.username_or_email,
        )
    ).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username/email or password")

    token = create_access_token(subject=str(user.id))
    return schemas.TokenResponse(access_token=token)