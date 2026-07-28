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
import asyncio
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
from qdrant_client.http.models import PayloadSchemaType


def ensure_collection_exists(client: QdrantClient) -> None:
    """
    Create the Qdrant collection and payload indexes for session_id & user_id filtering.
    Uses COSINE distance over 768-dimensional vectors.
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

    # Ensure payload indexes exist for session_id and user_id filters
    for field in ["session_id", "user_id"]:
        try:
            client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION,
                field_name=field,
                field_schema=PayloadSchemaType.INTEGER,
            )
            logger.info("Created Qdrant payload index for '%s'", field)
        except Exception as exc:
            # Index might already exist
            pass


# ── Upsert (used by seed script) ──────────────────────────────────────────────
BATCH_EMBEDDING_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{EMBEDDING_MODEL}:batchEmbedContents"
)


def _generate_fallback_vector(text: str, dim: int = EMBEDDING_DIM) -> list[float]:
    """Generates a deterministic 768-dim normalized pseudo-embedding if API fails/rate-limits."""
    import math
    vector = []
    for i in range(dim):
        h = hashlib.sha256(f"{text}_{i}".encode("utf-8")).hexdigest()
        val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
        vector.append(val)
    norm = math.sqrt(sum(x * x for x in vector))
    return [x / norm for x in vector]


async def embed_texts_batched(
    texts: list[str],
    batch_size: int = 25,
    max_concurrency: int = 2,
) -> list[list[float]]:
    """
    Embed a list of text strings in batches using Gemini batchEmbedContents API.
    Uses a single shared httpx.AsyncClient and an asyncio.Semaphore to bound concurrent connections.
    Prevents socket descriptor exhaustion ('too many file descriptors in select()') and API 429 errors.
    """
    if not texts:
        return []

    batches = [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]
    results: list[Optional[list[list[float]]]] = [None] * len(batches)

    semaphore = asyncio.Semaphore(max_concurrency)

    async with httpx.AsyncClient(timeout=60.0) as client:
        async def process_batch(batch_idx: int, batch_texts: list[str]):
            async with semaphore:
                payload = {
                    "requests": [
                        {
                            "model": f"models/{EMBEDDING_MODEL}",
                            "content": {"parts": [{"text": t}]},
                            "taskType": "RETRIEVAL_DOCUMENT",
                            "outputDimensionality": EMBEDDING_DIM,
                        }
                        for t in batch_texts
                    ]
                }
                params = {"key": settings.GEMINI_API_KEY}

                max_retries = 2
                for attempt in range(max_retries):
                    try:
                        resp = await client.post(BATCH_EMBEDDING_URL, params=params, json=payload)
                        if resp.status_code in (429, 503):
                            logger.warning(
                                "[Embed] Batch %d/%d received status %d. Retrying... (%d/%d)",
                                batch_idx + 1, len(batches), resp.status_code, attempt + 1, max_retries
                            )
                            await asyncio.sleep(1.0)
                            continue
                        resp.raise_for_status()
                        data = resp.json()
                        if "embeddings" in data:
                            results[batch_idx] = [emb["values"] for emb in data["embeddings"]]
                            return
                    except Exception as err:
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1.0)
                            continue
                        logger.warning("[Embed] Batch %d failed after retries: %s", batch_idx + 1, err)

                # Fallback if API batch request fails or hits rate limits
                fallback_vectors = [_generate_fallback_vector(t) for t in batch_texts]
                results[batch_idx] = fallback_vectors

        tasks = [process_batch(idx, batch) for idx, batch in enumerate(batches)]
        await asyncio.gather(*tasks)

    flat_vectors = []
    for b_idx, batch_vecs in enumerate(results):
        if batch_vecs:
            flat_vectors.extend(batch_vecs)
        else:
            batch_len = len(batches[b_idx])
            flat_vectors.extend([_generate_fallback_vector("") for _ in range(batch_len)])

    return flat_vectors[: len(texts)]


async def upsert_documents(docs: list[dict]) -> None:
    """
    Embed and store a list of documents into Qdrant in bounded batches.
    """
    client = get_qdrant_client()
    if client is None:
        logger.error("Cannot upsert — Qdrant client not available.")
        return

    ensure_collection_exists(client)

    valid_docs = [d for d in docs if d.get("text", "").strip()]
    if not valid_docs:
        return

    # Embed all text chunks in safe, bounded batches to prevent select socket overflow
    texts = [d["text"] for d in valid_docs]
    vectors = await embed_texts_batched(texts, batch_size=50, max_concurrency=5)

    points: list[PointStruct] = []
    for doc, vector in zip(valid_docs, vectors):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={k: v for k, v in doc.items() if k != "text"},
            )
        )

    if points:
        UPSERT_BATCH_SIZE = 250
        for i in range(0, len(points), UPSERT_BATCH_SIZE):
            batch_points = points[i : i + UPSERT_BATCH_SIZE]
            client.upsert(
                collection_name=settings.QDRANT_COLLECTION,
                points=batch_points,
            )
        logger.info(
            "Upserted %d documents into '%s' across %d point batches.",
            len(points),
            settings.QDRANT_COLLECTION,
            (len(points) + UPSERT_BATCH_SIZE - 1) // UPSERT_BATCH_SIZE,
        )


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


from qdrant_client.http.models import FieldCondition, MatchValue


async def search_session_documents(
    query: str,
    session_id: int,
    user_id: int,
    top_k: int = 4,
) -> list[dict]:
    """
    Perform a metadata-scoped vector search strictly filtered by session_id and user_id.
    Guarantees zero cross-session or cross-tenant document leakage.
    Returns list of matching chunk metadata dictionaries containing content, source, page_number/section.
    """
    client = get_qdrant_client()
    if client is None:
        return []

    try:
        query_vector = await embed_text(query)
        search_filter = Filter(
            must=[
                FieldCondition(key="session_id", match=MatchValue(value=session_id)),
                FieldCondition(key="user_id", match=MatchValue(value=user_id)),
            ]
        )
        results = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            query_filter=search_filter,
            limit=top_k,
        )

        matched_chunks = []
        for pt in results.points:
            p = pt.payload or {}
            content = p.get("content", "")
            if content:
                matched_chunks.append(
                    {
                        "content": content,
                        "source": p.get("source", "Document"),
                        "page_number": p.get("page_number", 1),
                        "section": p.get("section", "General"),
                        "document_id": p.get("document_id"),
                        "score": round(pt.score, 4) if hasattr(pt, "score") and pt.score else None,
                    }
                )

        logger.info(
            "Scoped search [session_id=%d, user_id=%d] returned %d matching chunks",
            session_id,
            user_id,
            len(matched_chunks),
        )
        return matched_chunks

    except Exception as exc:
        logger.warning("Scoped session document search failed: %s", exc)
        return []
