from app.config import settings
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStore
from app.utils.category_detector import detect_category


class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_service = LLMService()

    def build_context(self, results: list[dict]) -> str:
        context_parts = []

        for index, item in enumerate(results, start=1):
            source_file = item.get("source_file", "Unknown Source")
            chunk_index = item.get("chunk_index", 0)
            text = item.get("text", "")

            context_parts.append(
                f"[Dokumen {index}]\n"
                f"Sumber: {source_file}\n"
                f"Chunk: {chunk_index}\n"
                f"Isi:\n{text}"
            )

        return "\n\n".join(context_parts)

    def build_prompt(self, query: str, context: str) -> str:
        return f"""
            Anda adalah chatbot IT Support untuk membantu karyawan PT Finnet Indonesia.

            Tugas Anda:
            1. Jawab pertanyaan pengguna hanya berdasarkan konteks knowledge base yang diberikan.
            2. Jangan mengarang jawaban di luar konteks.
            3. Jika informasi tidak tersedia dalam konteks, jawab bahwa informasi belum tersedia di knowledge base.
            4. Berikan jawaban dalam bahasa Indonesia.
            5. Jika pertanyaan adalah panduan teknis atau troubleshooting, berikan jawaban dalam format Markdown numbered list dengan numbering: 1., 2., 3., dst.
            6. Pastikan setiap langkah dimulai dengan angka dan titik (contoh: "1. Buka portal...").
            7. Jawaban harus ringkas, jelas, dan mudah diikuti oleh karyawan non-teknis.

            === KONTEKS KNOWLEDGE BASE ===
            {context}

            === PERTANYAAN PENGGUNA ===
            {query}

            === JAWABAN ===
            """.strip()

    async def process_query(self, query: str) -> dict:
        results = self.vector_store.search(query, settings.TOP_K)

        if not results:
            return {
                "answer": "Maaf, informasi terkait pertanyaan Anda belum tersedia di knowledge base saat ini.",
                "sources": [],
                "category": "Umum",
                "similarity_score": 0.0,
                "is_fallback": True,
            }

        top_score = results[0]["similarity_score"]

        if top_score < settings.SIMILARITY_THRESHOLD:
            return {
                "answer": "Maaf, informasi terkait pertanyaan Anda belum tersedia di knowledge base saat ini.",
                "sources": [],
                "category": "Umum",
                "similarity_score": top_score,
                "is_fallback": True,
            }

        top_score = results[0]["similarity_score"]

        filtered_results = [
            item for item in results
            if item["similarity_score"] >= max(settings.SIMILARITY_THRESHOLD, top_score - 0.15)
        ]

        results = filtered_results

        context = self.build_context(results)
        prompt = self.build_prompt(query, context)

        answer = await self.llm_service.generate_answer(prompt)

        sources = list({item["source_file"] for item in results})
        category = detect_category(query, sources)

        return {
            "answer": answer,
            "sources": sources,
            "category": category,
            "similarity_score": top_score,
            "is_fallback": False,
        }