"""
Qdrant vector database service.

Responsibilities:
  - Initialize a Qdrant client using credentials from config
  - Embed text using Gemini text-embedding-004 (768 dimensions)
  - Create the collection if it doesn't exist
  - Upsert document points into the collection (used by seed script)
  - Search the collection semantically and return top-k payload texts
"""

import uuid
import logging
import httpx
import hashlib
import json
from typing import Optional

import redis as redis_lib
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Embedding config ──────────────────────────────────────────────────────────
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768                          # dimensions output by gemini-embedding-001
EMBEDDING_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{EMBEDDING_MODEL}:embedContent"
)

# ── Singleton Qdrant client ───────────────────────────────────────────────────
_client: Optional[QdrantClient] = None

# ── Redis cache client ────────────────────────────────────────────────────────
CACHE_TTL_SECONDS = 3600  # 1 hour — entries expire automatically

_redis_client: Optional[redis_lib.Redis] = None

def get_redis_client() -> Optional[redis_lib.Redis]:
    """
    Return a lazy singleton Redis client connected to localhost:6379.
    Returns None (and logs a warning) if Redis is not available so the app
    continues working without caching — Redis is an optimisation, not a hard dep.
    """
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    try:
        r = redis_lib.Redis(host="localhost", port=6379, db=0, socket_connect_timeout=1)
        r.ping()          # fails fast if Redis is down
        _redis_client = r
        logger.info("Redis cache connected → localhost:6379")
    except Exception as exc:
        logger.warning("Redis not available — caching disabled (%s)", exc)
        _redis_client = None
    return _redis_client


def _make_cache_key(query: str) -> str:
    """
    Produce a deterministic SHA-256 key for a normalised query string.
    Normalisation: strip surrounding whitespace, collapse inner whitespace,
    lowercase — so 'How many books  can I borrow?' and
    'how many books can i borrow?' map to the same key.
    """
    normalised = " ".join(query.strip().lower().split())
    digest = hashlib.sha256(normalised.encode()).hexdigest()
    return f"rag:kb:{digest}"


def get_qdrant_client() -> Optional[QdrantClient]:
    """Return the singleton Qdrant client. Returns None if credentials are not set."""
    global _client
    if _client is not None:
        return _client

    if not settings.QDRANT_URL or not settings.QDRANT_API_KEY:
        logger.warning("Qdrant credentials not configured — RAG search disabled.")
        return None

    _client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        timeout=10,
    )
    logger.info("Qdrant client initialized → %s", settings.QDRANT_URL)
    return _client


# ── Embedding helper ──────────────────────────────────────────────────────────
async def embed_text(text: str) -> list[float]:
    """
    Convert a text string into a 768-dimensional embedding vector
    using Gemini's gemini-embedding-001 model.

    The formula used internally is cosine similarity, so vectors are
    L2-normalised before being returned by the API — making DOT and
    COSINE distance equivalent for search.
    """
    payload = {
        "model": f"models/{EMBEDDING_MODEL}",
        "content": {"parts": [{"text": text}]},
        "taskType": "RETRIEVAL_DOCUMENT",
        "outputDimensionality": EMBEDDING_DIM,
    }
    params = {"key": settings.GEMINI_API_KEY}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(EMBEDDING_URL, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["embedding"]["values"]


# ── Collection management ─────────────────────────────────────────────────────
def ensure_collection_exists(client: QdrantClient) -> None:
    """
    Create the Qdrant collection if it does not exist.
    Uses COSINE distance over 768-dimensional vectors (matching text-embedding-004).
    """
    existing = [c.name for c in client.get_collections().collections]
    if settings.QDRANT_COLLECTION not in existing:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE,
            ),
        )
        logger.info("Created Qdrant collection '%s'", settings.QDRANT_COLLECTION)
    else:
        logger.info("Qdrant collection '%s' already exists.", settings.QDRANT_COLLECTION)


# ── Upsert (used by seed script) ──────────────────────────────────────────────
async def upsert_documents(docs: list[dict]) -> None:
    """
    Embed and store a list of documents into Qdrant.

    Each doc should be a dict with at least a 'text' key containing the
    content to embed, plus any metadata fields you want stored in the payload.

    Example doc:
        {
            "text": "Harry Potter — Fantasy — A young wizard discovers...",
            "title": "Harry Potter",
            "author": "J.K. Rowling",
            "genre": "Fantasy"
        }
    """
    client = get_qdrant_client()
    if client is None:
        logger.error("Cannot upsert — Qdrant client not available.")
        return

    ensure_collection_exists(client)

    points: list[PointStruct] = []
    for doc in docs:
        text = doc.get("text", "")
        if not text:
            continue
        vector = await embed_text(text)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={k: v for k, v in doc.items() if k != "text"},
            )
        )

    if points:
        client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )
        logger.info("Upserted %d documents into '%s'.", len(points), settings.QDRANT_COLLECTION)


# ── Semantic search with Redis exact-match caching ───────────────────────────
async def search_library(query: str, top_k: int = 3) -> list[str]:
    """
    Perform a semantic search against the library knowledge collection.

    Cache layer (exact-match, Redis):
      - The query is normalised (stripped + lowercased) and hashed with SHA-256.
      - On a CACHE HIT  → return the stored JSON list immediately.
        No embedding call, no Qdrant network round-trip.
      - On a CACHE MISS → run the full pipeline (embed → Qdrant), then store
        the result in Redis with a TTL of CACHE_TTL_SECONDS so entries expire
        automatically without any manual cleanup.

    Full pipeline steps (cache miss only):
      1. Embed the user's query with Gemini gemini-embedding-001
      2. Send the vector to Qdrant — returns top_k most similar points
      3. Extract and return the 'content' field from each matching payload

    Returns an empty list if Qdrant is not configured or search fails.
    Redis being unavailable is non-fatal — the function falls through to the
    normal pipeline transparently.
    """
    # ── 1. Check Redis cache ──────────────────────────────────────────────────
    redis = get_redis_client()
    cache_key = _make_cache_key(query)

    if redis is not None:
        try:
            cached = redis.get(cache_key)
            if cached is not None:
                logger.info("[Cache HIT]  key=%s  query=%r", cache_key[:16], query[:60])
                return json.loads(cached)
            logger.info("[Cache MISS] key=%s  query=%r", cache_key[:16], query[:60])
        except Exception as exc:
            logger.warning("Redis read error — falling through to Qdrant: %s", exc)

    # ── 2. Full retrieval pipeline (cache miss or Redis unavailable) ──────────
    client = get_qdrant_client()
    if client is None:
        return []

    try:
        query_vector = await embed_text(query)
        results = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=top_k,
        )
        # Extract the 'content' field stored in each point's payload
        contexts = []
        for pt in results.points:
            payload = pt.payload or {}
            content = payload.get("content", "")
            if content:
                contexts.append(content)

        # ── 3. Store result in Redis with TTL ─────────────────────────────────
        if redis is not None and contexts:
            try:
                redis.set(cache_key, json.dumps(contexts), ex=CACHE_TTL_SECONDS)
                logger.info(
                    "[Cache SET]  key=%s  ttl=%ds  chunks=%d",
                    cache_key[:16], CACHE_TTL_SECONDS, len(contexts)
                )
            except Exception as exc:
                logger.warning("Redis write error — result not cached: %s", exc)

        return contexts

    except Exception as exc:
        logger.warning("Qdrant search failed: %s — skipping RAG context.", exc)
        return []
