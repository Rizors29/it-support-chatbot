import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.config import settings
from app.models.response_models import RebuildIndexResponse
from app.services.vector_store import VectorStore
from app.utils.auth import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def rebuild_vector_index():
    vector_store = VectorStore()

    if vector_store.index_path.exists():
        os.remove(vector_store.index_path)

    if vector_store.metadata_path.exists():
        os.remove(vector_store.metadata_path)

    vector_store.get_or_build_index()

    return vector_store.get_index_size()


@router.post(
    "/rebuild-index",
    response_model=RebuildIndexResponse,
)
async def rebuild_index(
    current_user=Depends(require_admin),
):
    indexed_chunks = rebuild_vector_index()

    return RebuildIndexResponse(
        message="Index berhasil dibangun ulang.",
        indexed_chunks=indexed_chunks,
    )


@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(require_admin),
):
    allowed_extensions = [".pdf", ".txt", ".docx"]
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Format file tidak didukung. Gunakan PDF, TXT, atau DOCX.",
        )

    knowledge_base_path = Path(settings.KNOWLEDGE_BASE_PATH)
    knowledge_base_path.mkdir(parents=True, exist_ok=True)

    save_path = knowledge_base_path / file.filename

    with open(save_path, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

    indexed_chunks = rebuild_vector_index()

    return {
        "message": "Dokumen berhasil diupload dan index berhasil diperbarui.",
        "filename": file.filename,
        "indexed_chunks": indexed_chunks,
    }