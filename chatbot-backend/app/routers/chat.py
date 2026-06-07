from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models.request_models import ChatRequest
from app.models.response_models import (
    ChatResponse,
    HealthResponse,
)
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStore

router = APIRouter(prefix="", tags=["Chatbot"])

rag_service = RAGService()
vector_store = VectorStore()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query tidak boleh kosong.",
        )

    result = await rag_service.process_query(query)

    return ChatResponse(**result)


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    vector_store.get_or_build_index()

    return HealthResponse(
        status="ok",
        indexed_chunks=vector_store.get_index_size(),
        model=settings.GEMINI_MODEL,
    )