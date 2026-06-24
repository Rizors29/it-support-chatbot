import os
import shutil
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

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
    folder_name: str = Form(...),
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

    target_folder = knowledge_base_path / folder_name

    target_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_path = target_folder / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    indexed_chunks = rebuild_vector_index()

    return {
        "message": "Dokumen berhasil diupload dan index berhasil diperbarui.",
        "folder": folder_name,
        "filename": file.filename,
        "indexed_chunks": indexed_chunks,
    }


@router.get("/folders")
async def get_folders(
    current_user=Depends(require_admin),
):
    knowledge_base_path = Path(
        settings.KNOWLEDGE_BASE_PATH
    )

    folders = [
        folder.name
        for folder in knowledge_base_path.iterdir()
        if folder.is_dir()
    ]

    folders.sort()

    return {
        "folders": folders
    }


@router.get("/documents")
async def get_documents(
    current_user=Depends(require_admin),
):
    knowledge_base_path = Path(
        settings.KNOWLEDGE_BASE_PATH
    )

    folders = []

    for folder in sorted(knowledge_base_path.iterdir()):
        if folder.is_dir():

            files = []

            for file in sorted(folder.iterdir()):
                if file.is_file():
                    files.append({
                        "filename": file.name,
                        "size_kb": round(
                            file.stat().st_size / 1024,
                            2
                        )
                    })

            folders.append({
                "folder_name": folder.name,
                "files": files
            })

    return {
        "folders": folders
    }


@router.delete(
    "/documents/{folder_name}/{filename}"
)
async def delete_document(
    folder_name: str,
    filename: str,
    current_user=Depends(require_admin),
):
    file_path = (
        Path(settings.KNOWLEDGE_BASE_PATH)
        / folder_name
        / filename
    )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Dokumen tidak ditemukan.",
        )

    os.remove(file_path)

    indexed_chunks = rebuild_vector_index()

    return {
        "message": f"{filename} berhasil dihapus.",
        "indexed_chunks": indexed_chunks,
    }