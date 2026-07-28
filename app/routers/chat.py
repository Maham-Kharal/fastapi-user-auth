import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.services.orchestrator import orchestrate
from app.core.config import settings
from app.core.security import get_current_user
from app.core.database import get_db, SessionLocal
from app.services.cache import get_cached_reply, set_cached_reply
from app.services.moderation import is_blocked, REFUSAL_MESSAGE
from app.services.cerebras_client import call_cerebras
from app.services.gemini_client import SYSTEM_PROMPT
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
    res = await call_cerebras([{"role": "user", "content": request.message}])
    reply = res["choices"][0]["message"]["content"]
    usage = res.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    cost = (prompt_tokens / 1_000_000) * 0.05 + (completion_tokens / 1_000_000) * 0.25
    result = {
        "reply": reply,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost_usd": round(cost, 6)
    }

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

    # ---------------- Call Cerebras ----------------
    history = [
        {"role": m.role, "content": m.content}
        for m in history_rows
    ]

    res = await call_cerebras(history)
    reply = res["choices"][0]["message"]["content"]
    usage = res.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    cost = (prompt_tokens / 1_000_000) * 0.05 + (completion_tokens / 1_000_000) * 0.25
    result = {
        "reply": reply,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost_usd": round(cost, 6)
    }

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


# ============================================================
# Document Upload & Status Polling Endpoints
# ============================================================

from fastapi import UploadFile, File
import os
import uuid
from arq import create_pool
from arq.connections import RedisSettings
from app.models.models import Document
from app.services.document_parser import sniff_mime_type
from app.services.qdrant_service import search_session_documents

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit


@router.post("/sessions/{session_id}/upload")
async def upload_session_document(
    session_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a PDF or DOCX document to a chat session for scoped RAG grounding."""
    session = _get_owned_session(session_id, current_user, db)

    # 1. Read file content & enforce size limit
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum limit of 10MB.",
        )

    # 2. Real MIME-type magic bytes sniffing
    try:
        mime_type = sniff_mime_type(content)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )

    # 3. Save raw file to static/uploads/
    os.makedirs("static/uploads", exist_ok=True)
    safe_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join("static", "uploads", safe_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    # 4. Insert Document record in Postgres DB
    doc_row = Document(
        user_id=current_user.id,
        session_id=session.id,
        filename=file.filename,
        file_path=file_path,
        file_type=mime_type,
        file_size_bytes=len(content),
        status="processing",
    )
    db.add(doc_row)
    db.commit()
    db.refresh(doc_row)

    # 5. Enqueue ARQ ingestion job in Redis & spawn background processing fallback
    from app.worker import process_document_ingestion
    import asyncio

    try:
        redis = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
        await redis.enqueue_job("process_document_ingestion", doc_row.id)
    except Exception as exc:
        logger.error("Failed to enqueue document ingestion in Redis: %s", exc)

    # Spawn inline background task to guarantee document ingestion runs immediately
    asyncio.create_task(process_document_ingestion({}, doc_row.id))

    return {
        "document_id": doc_row.id,
        "filename": doc_row.filename,
        "file_type": doc_row.file_type,
        "file_size_bytes": doc_row.file_size_bytes,
        "status": doc_row.status,
    }


@router.get("/sessions/{session_id}/documents/{document_id}/status")
def get_document_status(
    session_id: int,
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Poll document processing status."""
    session = _get_owned_session(session_id, current_user, db)
    doc = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.session_id == session.id,
            Document.user_id == current_user.id,
        )
        .first()
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "error_message": doc.error_message,
        "created_at": doc.created_at,
    }


@router.get("/sessions/{session_id}/documents")
def list_session_documents(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all documents uploaded to a session."""
    session = _get_owned_session(session_id, current_user, db)
    docs = (
        db.query(Document)
        .filter(Document.session_id == session.id, Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "file_size_bytes": d.file_size_bytes,
            "status": d.status,
            "error_message": d.error_message,
            "created_at": d.created_at,
        }
        for d in docs
    ]


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

    # Check for session uploaded documents
    completed_docs = (
        db.query(Document)
        .filter(
            Document.session_id == session.id,
            Document.user_id == current_user.id,
            Document.status == "completed",
        )
        .all()
    )

    rag_context_parts = []
    scoped_doc_chunks = []

    if completed_docs:
        # Perform metadata-scoped search strictly isolated to this session_id and user_id
        try:
            scoped_doc_chunks = await search_session_documents(
                payload.content, session.id, current_user.id, top_k=4
            )
            rag_context_parts = [c["content"] for c in scoped_doc_chunks]
        except Exception as e:
            logger.warning("Scoped document RAG search failed: %s", e)
    else:
        # Fall back to global library search
        try:
            active_settings = get_active_chunking_settings()
            top_k = active_settings.get("top_k", 3)
            rag_context_parts = await search_library(payload.content, top_k=top_k)
        except Exception as e:
            logger.warning("RAG context lookup failed: %s", e)

    system_prompt = SYSTEM_PROMPT
    if scoped_doc_chunks:
        context_block = "\n".join(
            f"[{c['source']}, {c['section']}]: {c['content']}" for c in scoped_doc_chunks
        )
        system_prompt = (
            "You are a helpful assistant grounding your answers in the user's uploaded document.\n"
            "Use ONLY the document excerpts below to answer the user's question accurately.\n"
            "Cite your source for every claim using the format [Filename, Page X] or [Filename, Section Y].\n\n"
            "Document Excerpts:\n"
            + context_block
        )
    elif rag_context_parts:
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

        if completed_docs:
            if scoped_doc_chunks:
                # Direct grounded answer using Gemini / Cerebras with document system prompt
                try:
                    res = await call_cerebras(
                        messages=history,
                        system_prompt=system_prompt,
                        temperature=0.2,
                    )
                    choices = res.get("choices", [])
                    if choices:
                        full_reply = choices[0].get("message", {}).get("content", "")
                except Exception as e:
                    logger.warning("Cerebras QA failed (%s), falling back to Gemini...", e)

                if not full_reply:
                    try:
                        from app.services.gemini_client import ask_gemini
                        prompt_msg = f"{system_prompt}\n\nUser Question: {payload.content}"
                        gem_res = await ask_gemini([{"role": "user", "content": prompt_msg}])
                        gem_text = gem_res.get("reply", "") if isinstance(gem_res, dict) else str(gem_res)
                        if not gem_text or "experiencing high traffic" in gem_text or "429" in gem_text:
                            full_reply = f"Based on your uploaded document context:\n\n{context_block}"
                        else:
                            full_reply = gem_text
                    except Exception as ge:
                        full_reply = f"Based on your uploaded document context:\n\n{context_block}"

                yield f"data: {json.dumps({'chunk': full_reply})}\n\n"
            else:
                doc_name = completed_docs[0].filename
                full_reply = f"I searched your uploaded document ('{doc_name}'), but could not find information relevant to your question."
                yield f"data: {json.dumps({'chunk': full_reply})}\n\n"
        else:
            try:
                full_reply = await orchestrate(payload.content, current_user.id, db)
                yield f"data: {json.dumps({'chunk': full_reply})}\n\n"
            except Exception as e:
                stream_error = str(e)
                full_reply = f"⚠ {stream_error}"
                yield f"data: {json.dumps({'chunk': full_reply})}\n\n"

        elapsed = time.time() - start_time

        if full_reply:
            save_db = SessionLocal()
            try:
                save_db.add(ChatMessage(session_id=session_id_, role="assistant", content=full_reply))
                save_db.commit()
                logger.info("user=%s session=%d streamed reply saved (%d chars)", username, session_id_, len(full_reply))
            finally:
                save_db.close()

        # Grade RAG quality metrics
        try:
            metrics = await evaluate_rag_metrics(payload.content, rag_context_parts, full_reply)
        except Exception as e:
            logger.warning("evaluate_rag_metrics failed: %s", e)
            metrics = {"context_relevance": 0.0, "groundedness": 0.0, "answer_relevance": 0.0}

        history_char_count = sum(len(m["content"]) for m in history)
        prompt_tokens = int((len(system_prompt) + history_char_count) / 4)
        completion_tokens = int(len(full_reply) / 4)
        cost_usd = (prompt_tokens / 1_000_000) * 0.30 + (completion_tokens / 1_000_000) * 2.50

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

