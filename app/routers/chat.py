import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.database import get_db, SessionLocal
from app.services.cache import get_cached_reply, set_cached_reply
from app.services.moderation import is_blocked, REFUSAL_MESSAGE
from app.services.gemini_client import ask_gemini, stream_gemini, SYSTEM_PROMPT
from app.services.qdrant_service import search_library
from app.services.retrieval_eval import get_active_chunking_settings, evaluate_rag_metrics
import time
from app.schemas.schemas import (
    ChatRequest,
    ChatResponse,
    SessionCreate,
    SessionOut,
    MessageCreate,
    MessageOut,
    MessageReply,
)
from app.models.models import User, ChatSession, ChatMessage

logger = logging.getLogger("chat")
router = APIRouter(prefix="/chat", tags=["chat"])


# ============================================================
# Existing stateless endpoint — kept, only adapted to the new
# ask_gemini(messages: list) signature (was ask_gemini(str))
# ============================================================

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    result = await ask_gemini([{"role": "user", "content": request.message}])

    logger.info(
        "user=%s prompt_tokens=%d completion_tokens=%d cost_usd=%.6f",
        getattr(current_user, "username", current_user),
        result["prompt_tokens"],
        result["completion_tokens"],
        result["cost_usd"],
    )

    return ChatResponse(**result)


# ============================================================
# Helpers
# ============================================================

def _get_owned_session(session_id: int, current_user: User, db: Session) -> ChatSession:
    """
    Fetch a session, scoped to current_user. Returns 404 (not 403) if it
    exists but belongs to someone else — this avoids leaking whether a
    given session_id exists at all to a user who doesn't own it.
    """
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session


def _load_history(session_id: int, db: Session) -> list:
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
        .all()
    )
    return rows


# ============================================================
# Session-based endpoints (new)
# ============================================================

@router.post("/sessions", response_model=SessionOut)
def create_session(
    payload: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = ChatSession(user_id=current_user.id, title=payload.title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.get("/sessions/{session_id}/messages", response_model=List[MessageOut])
def get_session_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = _get_owned_session(session_id, current_user, db)
    return _load_history(session.id, db)

@router.get("/sessions", response_model=List[SessionOut])
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )

@router.post("/sessions/{session_id}/messages", response_model=MessageReply)
async def send_message(
    session_id: int,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = _get_owned_session(session_id, current_user, db)

    # Save the user's message
    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=payload.content,
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # ---------------- Guardrail ----------------
    if is_blocked(payload.content):
        assistant_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=REFUSAL_MESSAGE,
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)

        logger.info(
            "user=%s session=%d message BLOCKED by guardrail",
            current_user.username,
            session.id,
        )

        return MessageReply(
            reply=MessageOut.model_validate(assistant_msg),
            history=[
                MessageOut.model_validate(m)
                for m in _load_history(session.id, db)
            ],
        )

    # ---------------- Conversation History ----------------
    history_rows = _load_history(session.id, db)

    # ---------------- Cache Check ----------------
    if len(history_rows) == 1:
        cached = get_cached_reply(payload.content)
        if cached:
            assistant_msg = ChatMessage(
                session_id=session.id,
                role="assistant",
                content=cached,
            )
            db.add(assistant_msg)
            db.commit()
            db.refresh(assistant_msg)

            logger.info(
                "user=%s session=%d served from CACHE",
                current_user.username,
                session.id,
            )

            return MessageReply(
                reply=MessageOut.model_validate(assistant_msg),
                history=[
                    MessageOut.model_validate(m)
                    for m in history_rows + [assistant_msg]
                ],
            )

    # ---------------- Call Gemini ----------------
    history = [
        {"role": m.role, "content": m.content}
        for m in history_rows
    ]

    result = await ask_gemini(history)

    assistant_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=result["reply"],
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    # ---------------- Save Cache ----------------
    if len(history_rows) == 1:
        set_cached_reply(payload.content, result["reply"])

    logger.info(
        "user=%s session=%d prompt_tokens=%d completion_tokens=%d cost_usd=%.6f",
        current_user.username,
        session.id,
        result["prompt_tokens"],
        result["completion_tokens"],
        result["cost_usd"],
    )

    full_history = history_rows + [assistant_msg]

    return MessageReply(
        reply=MessageOut.model_validate(assistant_msg),
        history=[
            MessageOut.model_validate(m)
            for m in full_history
        ],
    )
     
@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = _get_owned_session(session_id, current_user, db)
    db.delete(session)
    db.commit()
    return {"detail": "Session deleted"}

@router.post("/sessions/{session_id}/stream")
async def stream_message(
    session_id: int,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = _get_owned_session(session_id, current_user, db)

    user_msg = ChatMessage(session_id=session.id, role="user", content=payload.content)
    db.add(user_msg)
    db.commit()

    session_id_ = session.id
    username = current_user.username

    # --- guardrail check ---
    if is_blocked(payload.content):
        logger.info("user=%s session=%d message BLOCKED by guardrail", username, session_id_)

        async def blocked_generator():
            save_db = SessionLocal()
            try:
                save_db.add(ChatMessage(session_id=session_id_, role="assistant", content=REFUSAL_MESSAGE))
                save_db.commit()
            finally:
                save_db.close()
            yield f"data: {json.dumps({'chunk': REFUSAL_MESSAGE})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(blocked_generator(), media_type="text/event-stream")
    # --- end guardrail check ---

    # RAG Context Retrieval using active chunking settings
    rag_context_parts = []
    try:
        active_settings = get_active_chunking_settings()
        # Retrieve top_k based on active configuration (default 3)
        top_k = active_settings.get("top_k", 3)
        rag_context_parts = await search_library(payload.content, top_k=top_k)
    except Exception as e:
        logger.warning("RAG context lookup failed: %s", e)

    system_prompt = SYSTEM_PROMPT
    if rag_context_parts:
        context_block = "\n".join(f"- {c}" for c in rag_context_parts)
        system_prompt = (
            SYSTEM_PROMPT
            + "\n\nRelevant library knowledge retrieved from database:\n"
            + context_block
            + "\nUse this information to give accurate, grounded answers."
        )

    history_rows = _load_history(session.id, db)
    history = [{"role": m.role, "content": m.content} for m in history_rows]

    async def event_generator():
        full_reply = ""
        stream_error = None
        start_time = time.time()
        try:
            async for chunk in stream_gemini(history, system_prompt_override=system_prompt):
                full_reply += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        except Exception as e:
            stream_error = str(e)
            yield f"data: {json.dumps({'chunk': f'⚠ {stream_error}'})}\n\n"

        elapsed = time.time() - start_time

        if full_reply:
            save_db = SessionLocal()
            try:
                save_db.add(ChatMessage(session_id=session_id_, role="assistant", content=full_reply))
                save_db.commit()
                logger.info("user=%s session=%d streamed reply saved (%d chars)", username, session_id_, len(full_reply))
            finally:
                save_db.close()

        # Grade RAG quality metrics — always send even if this fails
        try:
            metrics = await evaluate_rag_metrics(payload.content, rag_context_parts, full_reply)
        except Exception as e:
            logger.warning("evaluate_rag_metrics failed: %s", e)
            metrics = {"context_relevance": 0.0, "groundedness": 0.0, "answer_relevance": 0.0}

        # Estimate tokens and cost
        history_char_count = sum(len(m["content"]) for m in history)
        prompt_tokens = int((len(system_prompt) + history_char_count) / 4)
        completion_tokens = int(len(full_reply) / 4)
        cost_usd = (prompt_tokens / 1_000_000) * 0.30 + (completion_tokens / 1_000_000) * 2.50

        # Always send the metadata block — RAG metrics card depends on this
        metadata = {
            "latency_seconds": round(elapsed, 2),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_usd": round(cost_usd, 6),
            "retrieved_chunks": rag_context_parts,
            "metrics": metrics,
            "settings": get_active_chunking_settings(),
            "error": stream_error,
        }
        yield f"data: {json.dumps({'metadata': metadata})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

