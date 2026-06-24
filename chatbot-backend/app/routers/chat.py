from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_log_service import save_chat_log

from app.config import settings
from app.models.request_models import ChatRequest
from app.models.response_models import (
    ChatResponse,
    HealthResponse,
)
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStore
from app.utils.auth import get_optional_user

router = APIRouter(prefix="", tags=["Chatbot"])

vector_store = VectorStore()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_user)
):
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query tidak boleh kosong.",
        )

    rag_service = RAGService()
    result = await rag_service.process_query(
        query=query,
        model=request.model
    )
    
    save_chat_log(db, current_user, query, result)

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