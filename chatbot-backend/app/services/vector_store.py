import pickle
from pathlib import Path

import faiss

from app.config import settings
from app.services.document_loader import load_and_chunk_knowledge_base
from app.services.embedder import Embedder


class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        self.embedder = Embedder()

        self.vector_store_path = Path(settings.VECTOR_STORE_PATH)
        self.index_path = self.vector_store_path / "index.faiss"
        self.metadata_path = self.vector_store_path / "metadata.pkl"

        self.vector_store_path.mkdir(parents=True, exist_ok=True)

    def build_index(self, chunks_with_metadata: list[dict]) -> None:
        if not chunks_with_metadata:
            print("[WARNING] Tidak ada chunk untuk diindeks.")
            return

        texts = [chunk["text"] for chunk in chunks_with_metadata]
        embeddings = self.embedder.embed_texts(texts)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        self.metadata = chunks_with_metadata

        self.save_index()

        print(f"[INFO] Index berhasil dibuat dengan {len(self.metadata)} chunk.")

    def save_index(self) -> None:
        if self.index is None:
            return

        faiss.write_index(self.index, str(self.index_path))

        with open(self.metadata_path, "wb") as file:
            pickle.dump(self.metadata, file)

    def load_index(self) -> bool:
        if not self.index_path.exists() or not self.metadata_path.exists():
            return False

        self.index = faiss.read_index(str(self.index_path))

        with open(self.metadata_path, "rb") as file:
            self.metadata = pickle.load(file)

        print(f"[INFO] Index dimuat dengan {len(self.metadata)} chunk.")
        return True

    def get_or_build_index(self) -> None:
        loaded = self.load_index()

        if loaded:
            return

        print("[INFO] Index belum tersedia. Membuat index baru...")

        chunks = load_and_chunk_knowledge_base(settings.KNOWLEDGE_BASE_PATH)
        self.build_index(chunks)

    def search(self, query: str, top_k: int | None = None) -> list[dict]:
        if self.index is None:
            self.get_or_build_index()

        if self.index is None or self.index.ntotal == 0:
            return []

        top_k = top_k or settings.TOP_K

        query_embedding = self.embedder.embed_query(query)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, index_position in zip(scores[0], indices[0]):
            if index_position == -1:
                continue

            item = self.metadata[index_position].copy()
            item["similarity_score"] = float(score)
            results.append(item)

        return results

    def add_document_to_index(self, chunks_with_metadata: list[dict]) -> None:
        if not chunks_with_metadata:
            print("[WARNING] Tidak ada chunk baru untuk ditambahkan.")
            return

        if self.index is None:
            self.get_or_build_index()

        texts = [chunk["text"] for chunk in chunks_with_metadata]
        embeddings = self.embedder.embed_texts(texts)

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)
        self.metadata.extend(chunks_with_metadata)

        self.save_index()

        print(f"[INFO] {len(chunks_with_metadata)} chunk baru berhasil ditambahkan ke index.")

    def get_index_size(self) -> int:
        if self.index is None:
            self.load_index()

        if self.index is None:
            return 0

        return int(self.index.ntotal)