import os

from fastapi import APIRouter

from app.config import settings
from app.models.response_models import RebuildIndexResponse
from app.services.vector_store import VectorStore

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/rebuild-index",
    response_model=RebuildIndexResponse,
)
async def rebuild_index():

    vector_store = VectorStore()

    if vector_store.index_path.exists():
        os.remove(vector_store.index_path)

    if vector_store.metadata_path.exists():
        os.remove(vector_store.metadata_path)

    vector_store.get_or_build_index()

    return RebuildIndexResponse(
        message="Index berhasil dibangun ulang.",
        indexed_chunks=vector_store.get_index_size(),
    )