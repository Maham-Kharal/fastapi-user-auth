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
from typing import Optional

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


# ── Semantic search (used at chat time) ──────────────────────────────────────
async def search_library(query: str, top_k: int = 3) -> list[str]:
    """
    Perform a semantic search against the library knowledge collection.

    Steps:
      1. Embed the user's query with Gemini gemini-embedding-001
      2. Send the vector to Qdrant — it returns the top_k most similar points
         ranked by cosine similarity score (higher = more relevant)
      3. Extract and return the 'content' field from each matching payload

    Returns an empty list if Qdrant is not configured or search fails.
    """
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
        return contexts

    except Exception as exc:
        logger.warning("Qdrant search failed: %s — skipping RAG context.", exc)
        return []
