from __future__ import annotations

import os
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.document_loader import load_and_chunk_knowledge_base


class VectorStore:
    def __init__(self) -> None:
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        self.metadata: list[dict] = []

        self.vector_store_path = Path(settings.VECTOR_STORE_PATH)
        self.vectorizer_path = self.vector_store_path / "vectorizer.pkl"
        self.matrix_path = self.vector_store_path / "matrix.pkl"
        self.metadata_path = self.vector_store_path / "metadata.pkl"

        self.vector_store_path.mkdir(parents=True, exist_ok=True)

    def build_index(self, chunks_with_metadata: list[dict]) -> None:
        if not chunks_with_metadata:
            print("[WARNING] Tidak ada chunk untuk diindeks.")
            return

        texts = [chunk["text"] for chunk in chunks_with_metadata]
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=20000,
        )
        self.matrix = self.vectorizer.fit_transform(texts)
        self.metadata = chunks_with_metadata

        self.save_index()
        print(f"[INFO] Index berhasil dibuat dengan {len(self.metadata)} chunk.")

    def save_index(self) -> None:
        if self.vectorizer is None or self.matrix is None:
            return

        with open(self.vectorizer_path, "wb") as file:
            pickle.dump(self.vectorizer, file)

        with open(self.matrix_path, "wb") as file:
            pickle.dump(self.matrix, file)

        with open(self.metadata_path, "wb") as file:
            pickle.dump(self.metadata, file)

    def clear_index_files(self) -> None:
        for path in (self.vectorizer_path, self.matrix_path, self.metadata_path):
            if path.exists():
                os.remove(path)

        self.vectorizer = None
        self.matrix = None
        self.metadata = []

    def load_index(self) -> bool:
        if not (
            self.vectorizer_path.exists()
            and self.matrix_path.exists()
            and self.metadata_path.exists()
        ):
            return False

        with open(self.vectorizer_path, "rb") as file:
            self.vectorizer = pickle.load(file)

        with open(self.matrix_path, "rb") as file:
            self.matrix = pickle.load(file)

        with open(self.metadata_path, "rb") as file:
            self.metadata = pickle.load(file)

        print(f"[INFO] Index dimuat dengan {len(self.metadata)} chunk.")
        return True

    def get_or_build_index(self) -> None:
        if self.load_index():
            return

        print("[INFO] Index belum tersedia. Membuat index baru...")
        chunks = load_and_chunk_knowledge_base(settings.KNOWLEDGE_BASE_PATH)
        self.build_index(chunks)

    def rebuild_index(self) -> None:
        self.clear_index_files()
        chunks = load_and_chunk_knowledge_base(settings.KNOWLEDGE_BASE_PATH)
        self.build_index(chunks)

    def search(self, query: str, top_k: int | None = None) -> list[dict]:
        if self.vectorizer is None or self.matrix is None:
            self.get_or_build_index()

        if self.vectorizer is None or self.matrix is None or not self.metadata:
            return []

        top_k = top_k or settings.TOP_K
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]

        ranked_indices = scores.argsort()[::-1][:top_k]
        results: list[dict] = []

        for index_position in ranked_indices:
            score = float(scores[index_position])
            if index_position < 0:
                continue

            item = self.metadata[index_position].copy()
            item["similarity_score"] = score
            results.append(item)

        return results

    def get_index_size(self) -> int:
        if self.vectorizer is None or self.matrix is None:
            self.load_index()

        if self.matrix is None:
            return 0

        return int(self.matrix.shape[0])
