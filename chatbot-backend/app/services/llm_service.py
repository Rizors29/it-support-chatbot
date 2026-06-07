from app.config import settings
from app.services.groq_service import GroqService


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER

        if self.provider == "groq":
            self.service = GroqService()
        elif self.provider == "mock":
            self.service = None
        else:
            from app.services.gemini_service import GeminiService
            self.service = GeminiService()

    async def generate_answer(self, prompt: str) -> str:
        if self.provider == "mock":
            return self.generate_mock_answer(prompt)

        return await self.service.generate_answer(prompt)

    def generate_mock_answer(self, prompt: str) -> str:
        context = self.extract_context_from_prompt(prompt)
        cleaned_context = self.clean_mock_context(context)

        return (
            "**Mode mock aktif**\n\n"
            "Jawaban berikut diambil dari hasil retrieval knowledge base:\n\n"
            f"{cleaned_context}\n\n"
            "_Catatan: Mode ini tidak menggunakan API LLM, sehingga tidak mengurangi kuota model._"
        )

    def extract_context_from_prompt(self, prompt: str) -> str:
        try:
            context = prompt.split("=== KONTEKS KNOWLEDGE BASE ===")[1]
            context = context.split("=== PERTANYAAN PENGGUNA ===")[0]
            return context.strip()
        except IndexError:
            return prompt[:1200]

    def clean_mock_context(self, context: str) -> str:
        import re

        context = context.replace("[Dokumen 1]", "")
        context = context.replace("Chunk: 0", "")
        context = context.replace("Isi:", "")
        context = context.strip()

        context = re.sub(r"Sumber:\s*", "**Sumber:** ", context)
        context = re.sub(r"\s(?=\d+\.\s)", "\n", context)
        context = re.sub(r"[ \t]+", " ", context)
        context = re.sub(r"\n+", "\n", context)

        return context[:1500].strip()