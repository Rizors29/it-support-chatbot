from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Chatbot IT Support Fullstack")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    HF_API_KEY = os.getenv("HF_API_KEY")
    HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen3-8B:nscale")

    KNOWLEDGE_BASE_PATH = os.getenv(
        "KNOWLEDGE_BASE_PATH",
        str(BASE_DIR / "knowledge_base"),
    )
    VECTOR_STORE_PATH = os.getenv(
        "VECTOR_STORE_PATH",
        str(BASE_DIR / "vector_store"),
    )

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K = int(os.getenv("TOP_K", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.12"))
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))


settings = Settings()


def validate_settings() -> None:
    placeholders = {
        "",
        "your_gemini_api_key",
        "your_gemini_api_key_here",
        "your_groq_api_key",
        "your_groq_api_key_here",
        "your_huggingface_api_key",
        "your_huggingface_api_key_here",
    }

    provider = settings.LLM_PROVIDER
    if provider not in {"mock", "gemini", "groq", "llama", "qwen"}:
        raise RuntimeError(
            f"LLM_PROVIDER tidak valid: {provider}. Pilihan: mock, gemini, groq, llama, qwen."
        )

    if settings.USE_MOCK_LLM or provider == "mock":
        return

    if provider == "gemini" and (not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY in placeholders):
        raise RuntimeError("GEMINI_API_KEY belum diisi dengan benar di file .env")

    if provider in {"groq", "llama"} and (not settings.GROQ_API_KEY or settings.GROQ_API_KEY in placeholders):
        raise RuntimeError("GROQ_API_KEY belum diisi dengan benar di file .env")

    if provider == "qwen" and (not settings.HF_API_KEY or settings.HF_API_KEY in placeholders):
        raise RuntimeError("HF_API_KEY belum diisi dengan benar di file .env")

