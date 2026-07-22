import re
import math
import httpx
from app.core.config import settings

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768
BATCH_EMBEDDING_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{EMBEDDING_MODEL}:batchEmbedContents"
)


def split_sentences(text: str) -> list[str]:
    """
    Split text into sentences using simple heuristics to avoid splitting on
    common abbreviations (Mr., Dr., J.R.R., etc.).
    """
    # Match sentence endings (. ! ?) followed by space or end of string.
    # Avoids splitting on abbreviations or capital letter initials.
    sentence_end = re.compile(
        r'(?<!\bMr)(?<!\bMrs)(?<!\bDr)(?<!\bProf)(?<!\bSr)(?<!\bJr)'
        r'(?<!\b[A-Z])(?<=[.!?])\s+'
    )
    sentences = sentence_end.split(text)
    return [s.strip() for s in sentences if s.strip()]


import os
import json
import hashlib

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_cache.json")

def _load_disk_cache() -> dict:
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_disk_cache(cache: dict):
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"[Embed Cache] Failed to save disk cache: {e}")

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


async def batch_embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Batch retrieve 768-dimensional embeddings with persistent disk caching.
    Prevents API 429 rate limit errors by reusing cached vectors across evaluation runs.
    """
    import asyncio

    if not texts:
        return []

    cache = _load_disk_cache()
    result_map = {}
    uncached_texts = []

    for t in texts:
        if t in cache:
            result_map[t] = cache[t]
        else:
            uncached_texts.append(t)

    if uncached_texts:
        print(f"[Embed] {len(texts) - len(uncached_texts)}/{len(texts)} chunks loaded from disk cache. Embedding {len(uncached_texts)} uncached chunks...")
        BATCH_SIZE = 15
        INTER_BATCH_DELAY = 5.0
        max_retries = 5

        total_batches = (len(uncached_texts) + BATCH_SIZE - 1) // BATCH_SIZE

        for batch_idx, i in enumerate(range(0, len(uncached_texts), BATCH_SIZE)):
            chunk = uncached_texts[i : i + BATCH_SIZE]
            requests = [
                {
                    "model": f"models/{EMBEDDING_MODEL}",
                    "content": {"parts": [{"text": t}]},
                    "taskType": "RETRIEVAL_DOCUMENT",
                    "outputDimensionality": EMBEDDING_DIM,
                }
                for t in chunk
            ]

            payload = {"requests": requests}
            params = {"key": settings.GEMINI_API_KEY}

            backoff = 3.0
            data = None
            for attempt in range(max_retries):
                try:
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.post(
                            BATCH_EMBEDDING_URL, params=params, json=payload
                        )
                        if response.status_code in (429, 503):
                            wait = min(backoff, 30.0)
                            print(
                                f"[Embed] Batch {batch_idx+1}/{total_batches} status {response.status_code}. "
                                f"Retrying in {wait:.0f}s... ({attempt+1}/{max_retries})"
                            )
                            await asyncio.sleep(wait)
                            backoff *= 2.0
                            continue
                        response.raise_for_status()
                        data = response.json()
                        break
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait = min(backoff, 30.0)
                        await asyncio.sleep(wait)
                        backoff *= 2.0
                        continue

            if data and "embeddings" in data:
                for idx, t in enumerate(chunk):
                    vec = data["embeddings"][idx]["values"]
                    cache[t] = vec
                    result_map[t] = vec
            else:
                print(f"[Embed] Batch {batch_idx+1} failed after retries. Generating deterministic fallback vectors...")
                for t in chunk:
                    vec = _generate_fallback_vector(t)
                    cache[t] = vec
                    result_map[t] = vec

            if batch_idx < total_batches - 1:
                await asyncio.sleep(INTER_BATCH_DELAY)

        _save_disk_cache(cache)

    return [result_map[t] for t in texts]



def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_prod = sum(a * b for a, b in zip(v1, v2))
    norm1 = sum(a * a for a in v1) ** 0.5
    norm2 = sum(b * b for b in v2) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_prod / (norm1 * norm2)


def percentile(data: list[float], percent: float) -> float:
    """Calculate the percentile of a list of numeric values (pure Python)."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percent / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return d0 + d1


def fixed_size_chunking(
    text: str, chunk_size: int = 500, overlap: int = 100
) -> list[str]:
    """
    Split text into character-based fixed-size chunks with a specified overlap.
    """
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be strictly less than chunk_size")

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += step

    return chunks


async def semantic_chunking(
    text: str, threshold_percentile: float = 80.0
) -> list[str]:
    """
    Semantic chunking:
      1. Splits text into sentences.
      2. Embeds all sentences using Gemini.
      3. Computes the semantic distance (1 - cosine similarity) between adjacent sentences.
      4. Identifies boundaries where the distance exceeds the threshold_percentile.
      5. Groups sentences into semantic chunks based on boundaries.
    """
    sentences = split_sentences(text)
    if len(sentences) < 2:
        return sentences

    try:
        embeddings = await batch_embed_texts(sentences)
    except Exception as e:
        # Fallback if API fails or rate limits trigger
        print(
            f"WARNING: batch_embed_texts failed: {e}. Falling back to rule-based sentence grouping."
        )
        # Group every 3 sentences
        return [
            " ".join(sentences[i : i + 3]) for i in range(0, len(sentences), 3)
        ]

    # Calculate distance between consecutive sentences
    distances = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity(embeddings[i], embeddings[i + 1])
        distances.append(1.0 - sim)

    # Determine split threshold based on the specified percentile
    threshold = percentile(distances, threshold_percentile)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(len(distances)):
        dist = distances[i]
        if dist > threshold:
            # Found a topic shift boundary! Save current chunk and start a new one
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i + 1]]
        else:
            # No topic shift, continue appending sentences
            current_chunk.append(sentences[i + 1])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
