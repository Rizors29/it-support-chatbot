import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K = int(os.getenv("TOP_K", 5))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.4))

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 20))

    USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey123")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()

def validate_settings():
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_api_key_here":
        raise RuntimeError("GEMINI_API_KEY belum diisi di file .env")