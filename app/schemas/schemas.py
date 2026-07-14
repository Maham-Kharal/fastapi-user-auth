from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# ============================================================
# Auth / User schemas
# ============================================================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================================================
# Old stateless chat schemas (existing /chat endpoint — untouched)
# ============================================================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float


# ============================================================
# Chat session schemas (new)
# ============================================================

class SessionCreate(BaseModel):
    title: Optional[str] = None


class SessionOut(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# Chat message schemas (new)
# ============================================================

class MessageCreate(BaseModel):
    content: str


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageReply(BaseModel):
    """What /messages returns: the assistant's reply + full history"""
    reply: MessageOut
    history: List[MessageOut]