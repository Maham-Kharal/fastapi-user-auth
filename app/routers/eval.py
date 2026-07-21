from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid

from app.core.security import get_current_user
from app.core.config import settings
from app.services.corpus import RAW_DOCUMENTS
from app.services.chunking import fixed_size_chunking, semantic_chunking, batch_embed_texts
from app.services.qdrant_service import get_qdrant_client
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from app.services.retrieval_eval import (
    set_active_chunking_settings,
    get_active_chunking_settings,
    run_eval_harness_logic,
)

router = APIRouter(prefix="/eval", tags=["evaluation"])


class ReindexRequest(BaseModel):
    strategy: str  # "fixed" or "semantic"
    chunk_size: int = 500
    overlap: int = 100


@router.get("/settings")
def get_settings(current_user=Depends(get_current_user)):
    """Return the active chunking settings."""
    return get_active_chunking_settings()


@router.post("/reindex")
async def reindex_database(
    payload: ReindexRequest, current_user=Depends(get_current_user)
):
    """
    Clears the active Qdrant collection and re-indexes the library corpus
    using the specified chunking strategy, size, and overlap.
    """
    client = get_qdrant_client()
    if client is None:
        raise HTTPException(status_code=500, detail="Qdrant client not available")

    # 1. Chunk documents based on parameters
    chunks = []
    for doc in RAW_DOCUMENTS:
        if payload.strategy == "fixed":
            doc_chunks = fixed_size_chunking(
                doc["text"], chunk_size=payload.chunk_size, overlap=payload.overlap
            )
        else:
            doc_chunks = await semantic_chunking(doc["text"], threshold_percentile=80)

        for chunk_text in doc_chunks:
            chunks.append({"text": chunk_text, "doc_id": doc["id"]})

    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks generated")

    try:
        # 2. Reset active collection in Qdrant
        try:
            client.delete_collection(settings.QDRANT_COLLECTION)
        except Exception:
            pass

        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

        # 3. Batch embed and upload chunks
        chunk_texts = [c["text"] for c in chunks]
        vectors = await batch_embed_texts(chunk_texts)

        points = []
        for idx, c in enumerate(chunks):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vectors[idx],
                    payload={"content": c["text"], "doc_id": c["doc_id"]},
                )
            )

        client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)

        # 4. Save settings state in memory
        set_active_chunking_settings(
            payload.strategy, payload.chunk_size, payload.overlap
        )

        return {
            "status": "success",
            "chunks_indexed": len(points),
            "strategy": payload.strategy,
            "chunk_size": payload.chunk_size,
            "overlap": payload.overlap,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Re-indexing failed: {str(e)}")


@router.post("/run")
async def run_evaluation(current_user=Depends(get_current_user)):
    """
    Executes the full comparative RAG evaluation harness across 5 configurations
    and returns a summary + detailed query hit logs.
    """
    try:
        result = await run_eval_harness_logic(write_report_file=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
