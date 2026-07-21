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


async def batch_embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Batch retrieve 768-dimensional embeddings from Gemini's batchEmbedContents.
    Splits requests into chunks of 100 to stay within API batch limits.
    Includes robust exponential backoff retry logic to handle 429 Rate Limits.
    """
    if not texts:
        return []

    embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        chunk = texts[i : i + batch_size]
        requests = []
        for t in chunk:
            requests.append(
                {
                    "model": f"models/{EMBEDDING_MODEL}",
                    "content": {"parts": [{"text": t}]},
                    "taskType": "RETRIEVAL_DOCUMENT",
                    "outputDimensionality": EMBEDDING_DIM,
                }
            )

        payload = {"requests": requests}
        params = {"key": settings.GEMINI_API_KEY}

        import asyncio
        max_retries = 5
        backoff = 2.0
        data = None
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        BATCH_EMBEDDING_URL, params=params, json=payload
                    )
                    if response.status_code in (429, 503):
                        if attempt < max_retries - 1:
                            print(f"Embedding API returned status {response.status_code}. Retrying in {backoff}s... (Attempt {attempt+1}/{max_retries})")
                            await asyncio.sleep(backoff)
                            backoff *= 2.0
                            continue
                    response.raise_for_status()
                    data = response.json()
                    break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Embedding API exception: {e}. Retrying in {backoff}s... (Attempt {attempt+1}/{max_retries})")
                    await asyncio.sleep(backoff)
                    backoff *= 2.0
                    continue
                raise e

        if data is None:
            raise Exception("Failed to get embeddings after retries")

        embeddings.extend([emb["values"] for emb in data["embeddings"]])

    return embeddings


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
