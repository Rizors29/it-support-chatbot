import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Gemini API configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # GROQ API configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # Hugging Face API configuration
    HF_API_KEY = os.getenv("HF_API_KEY")
    HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen3-8B:nscale")

    # Path configurations
    KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")

    # LLM configurations
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K = int(os.getenv("TOP_K", 5))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.4))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 20))
    USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"

    # Database configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey123")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()

def validate_settings():
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        raise RuntimeError("GEMINI_API_KEY belum diisi di file .env")
    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
        raise RuntimeError("GROQ_API_KEY belum diisi di file .env")
    if not settings.HF_API_KEY or settings.HF_API_KEY == "your_huggingface_api_key_here":
        raise RuntimeError("HF_API_KEY belum diisi di file .env")
    if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY == "your_jwt_secret_key_here":
        raise RuntimeError("JWT_SECRET_KEY belum diisi di file .env")