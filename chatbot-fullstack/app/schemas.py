from __future__ import annotations

from pydantic import BaseModel, Field

from app.config import settings


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Pertanyaan pengguna")
    model: str = Field(default=settings.LLM_PROVIDER, description="mock, gemini, groq/llama, qwen")


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    category: str
    similarity_score: float
    is_fallback: bool


class HealthResponse(BaseModel):
    status: str
    indexed_chunks: int
    provider: str
    model: str

