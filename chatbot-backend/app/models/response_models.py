from pydantic import BaseModel


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    category: str
    similarity_score: float
    is_fallback: bool


class HealthResponse(BaseModel):
    status: str
    indexed_chunks: int
    model: str


class RebuildIndexResponse(BaseModel):
    message: str
    indexed_chunks: int