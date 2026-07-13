from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.models import User

router = APIRouter(tags=["chat"])


class ConnectionManager:
    def __init__(self):
        self.active: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active.pop(user_id, None)

    async def broadcast(self, message: str):
        for ws in self.active.values():
            await ws.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    token = websocket.query_params.get("token")
    user_id = decode_access_token(token) if token else None

    if not user_id:
        # Reject before accepting — the client never gets a usable connection
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == int(user_id)).first()
    db.close()
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user.id, websocket)
    await manager.broadcast(f"{user.username} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user.id)
        await manager.broadcast(f"{user.username} left the chat")