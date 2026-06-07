import asyncio
import re

import google.generativeai as genai
from fastapi import HTTPException

from app.config import settings


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=1024,
            ),
        )

    def extract_context_from_prompt(self, prompt: str) -> str:
        try:
            context = prompt.split("=== KONTEKS KNOWLEDGE BASE ===")[1]
            context = context.split("=== PERTANYAAN PENGGUNA ===")[0]
            return context.strip()
        except IndexError:
            return prompt[:1200]
        
    def clean_mock_context(self, context: str) -> str:
        context = context.replace("[Dokumen 1]", "")
        context = context.replace("Chunk: 0", "")
        context = context.replace("Isi:", "")
        context = context.strip()

        context = re.sub(r"Sumber:\s*", "**Sumber:** ", context)

        # Pisahkan nomor langkah 1. 2. 3. menjadi baris baru
        context = re.sub(r"\s(?=\d+\.\s)", "\n", context)

        # Rapikan spasi berlebih
        context = re.sub(r"[ \t]+", " ", context)
        context = re.sub(r"\n+", "\n", context)

        return context[:1500].strip()
    
    async def generate_answer(self, prompt: str) -> str:
        if settings.USE_MOCK_LLM:
            context = self.extract_context_from_prompt(prompt)
            cleaned_context = self.clean_mock_context(context)

            return (
                "**Mode mock aktif**\n\n"
                "Jawaban berikut diambil dari hasil retrieval knowledge base:\n\n"
                f"{cleaned_context}\n\n"
                "_Catatan: Mode ini tidak menggunakan Gemini API, sehingga tidak mengurangi kuota model._"
            )
        try:                      
            response = await asyncio.wait_for(
                asyncio.to_thread(self.model.generate_content, prompt),
                timeout=30.0,
            )

            if not response or not response.text:
                raise HTTPException(
                    status_code=503,
                    detail="Respons kosong dari Gemini API.",
                )

            return response.text.strip()

        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=503,
                detail="Gemini API tidak merespons dalam 30 detik.",
            )

        except HTTPException:
            raise

        except Exception as error:
            raise HTTPException(
                status_code=503,
                detail=f"Terjadi error saat memanggil Gemini API: {str(error)}",
            )