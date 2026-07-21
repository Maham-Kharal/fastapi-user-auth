import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.models import User
from app.services.orchestrator import run_orchestrator as orchestrate

router = APIRouter(tags=["chat"])


@router.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    token = websocket.query_params.get("token")
    user_id = decode_access_token(token) if token else None

    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == int(user_id)).first()
    db.close()
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    # in-memory conversation history for this single connection
    history: list[dict] = []

    try:
        while True:
            user_message = await websocket.receive_text()
            history.append({"role": "user", "content": user_message})

            db = SessionLocal()
            try:
                reply = await orchestrate(user_message, user.id, db)
                result = {"reply": reply}
            except Exception as e:
                result = {"reply": f"Sorry, something went wrong: {str(e)}"}
            finally:
                db.close()

            history.append({"role": "assistant", "content": result["reply"]})
            await websocket.send_text(result["reply"])

    except WebSocketDisconnect:
        pass