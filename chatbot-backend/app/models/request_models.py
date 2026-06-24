from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Pertanyaan pengguna",
    )

    model: str = Field(
        default="llama",
        description="Model yang digunakan: llama, gemini, qwen",
    )