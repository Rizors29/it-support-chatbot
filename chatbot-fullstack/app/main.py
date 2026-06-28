from __future__ import annotations

from pathlib import Path

import shutil
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings, validate_settings
from app.rag import RAGService
from app.schemas import ChatRequest, ChatResponse, HealthResponse


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title=settings.APP_NAME,
    description="Aplikasi chatbot IT Support fullstack Python dengan RAG",
    version=settings.APP_VERSION,
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
rag_service = RAGService()

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
def startup_event() -> None:
    validate_settings()
    print(f"{settings.APP_NAME} berjalan.")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "default_provider": settings.LLM_PROVIDER,
            "providers": ["mock", "gemini", "groq", "llama", "qwen"],
        },
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await rag_service.process_query(
        query=request.query.strip(),
        model=request.model,
    )
    return ChatResponse(**result)


@app.get("/health", response_model=HealthResponse)
def health_check():
    rag_service.vector_store.get_or_build_index()
    return HealthResponse(
        status="ok",
        indexed_chunks=rag_service.vector_store.get_index_size(),
        provider=settings.LLM_PROVIDER,
        model=settings.GEMINI_MODEL if settings.LLM_PROVIDER == "gemini" else (
            settings.GROQ_MODEL if settings.LLM_PROVIDER in {"groq", "llama"} else (
                settings.HF_MODEL if settings.LLM_PROVIDER == "qwen" else "mock"
            )
        ),
    )


@app.get("/api/folders")
def list_folders():
    base_path = Path(settings.KNOWLEDGE_BASE_PATH)
    base_path.mkdir(parents=True, exist_ok=True)

    folders = sorted([folder.name for folder in base_path.iterdir() if folder.is_dir()])
    return {"folders": folders}


@app.get("/api/documents")
def list_documents():
    base_path = Path(settings.KNOWLEDGE_BASE_PATH)
    base_path.mkdir(parents=True, exist_ok=True)

    folders = []

    for folder in sorted(base_path.iterdir()):
        if not folder.is_dir():
            continue

        files = []
        for file in sorted(folder.iterdir()):
            if file.is_file():
                files.append(
                    {
                        "filename": file.name,
                        "size_kb": round(file.stat().st_size / 1024, 2),
                    }
                )

        folders.append({"folder_name": folder.name, "files": files})

    return {"folders": folders}


@app.post("/api/upload-document")
async def upload_document(
    folder_name: str = Form(...),
    file: UploadFile = File(...),
):
    allowed_extensions = {".pdf", ".txt", ".docx"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Format file tidak didukung. Gunakan PDF, TXT, atau DOCX.",
        )

    safe_folder = Path(folder_name.strip()).name
    if not safe_folder or safe_folder in {".", ".."}:
        raise HTTPException(status_code=400, detail="Nama folder tidak valid.")

    knowledge_base_path = Path(settings.KNOWLEDGE_BASE_PATH)
    target_folder = knowledge_base_path / safe_folder
    target_folder.mkdir(parents=True, exist_ok=True)

    save_path = target_folder / Path(file.filename).name

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rag_service.vector_store.rebuild_index()

    return {
        "message": "Dokumen berhasil diupload dan index berhasil diperbarui.",
        "folder": safe_folder,
        "filename": save_path.name,
        "indexed_chunks": rag_service.vector_store.get_index_size(),
    }


@app.get("/api/index")
def index_status():
    rag_service.vector_store.get_or_build_index()
    return {
        "indexed_chunks": rag_service.vector_store.get_index_size(),
        "knowledge_base_path": settings.KNOWLEDGE_BASE_PATH,
        "vector_store_path": settings.VECTOR_STORE_PATH,
    }
