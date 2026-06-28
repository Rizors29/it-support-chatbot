from __future__ import annotations

import asyncio
import re

import google.generativeai as genai
import requests
from groq import Groq
from fastapi import HTTPException

from app.config import settings


class LLMService:
    def __init__(self, provider: str):
        self.provider = provider.lower()

        if self.provider == "llama":
            self.provider = "groq"

        if self.provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise RuntimeError("GEMINI_API_KEY belum diisi di file .env")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=1024,
                ),
            )
        elif self.provider == "groq":
            if not settings.GROQ_API_KEY:
                raise RuntimeError("GROQ_API_KEY belum diisi di file .env")
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = settings.GROQ_MODEL
        elif self.provider == "qwen":
            if not settings.HF_API_KEY:
                raise RuntimeError("HF_API_KEY belum diisi di file .env")
            self.api_url = "https://router.huggingface.co/v1/chat/completions"
            self.model = settings.HF_MODEL
        elif self.provider == "mock":
            self.model = "mock"
        else:
            raise ValueError(
                "Provider LLM tidak valid. Pilihan yang valid adalah: mock, gemini, groq, llama, qwen."
            )

    async def generate_answer(self, prompt: str) -> str:
        if self.provider == "mock":
            return self.generate_mock_answer(prompt)
        if self.provider == "gemini":
            return await self.generate_gemini_answer(prompt)
        if self.provider == "groq":
            return await self.generate_groq_answer(prompt)
        if self.provider == "qwen":
            return await self.generate_qwen_answer(prompt)

        raise RuntimeError("Provider LLM tidak didukung.")

    async def generate_gemini_answer(self, prompt: str) -> str:
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(self.model.generate_content, prompt),
                timeout=30.0,
            )

            if not response or not response.text:
                raise HTTPException(status_code=503, detail="Respons kosong dari Gemini API.")

            return response.text.strip()
        except asyncio.TimeoutError:
            raise HTTPException(status_code=503, detail="Gemini API tidak merespons dalam 30 detik.")
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(status_code=503, detail=f"Terjadi error saat memanggil Gemini API: {error}")

    async def generate_groq_answer(self, prompt: str) -> str:
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Anda adalah chatbot IT Support. "
                                "Jawab hanya berdasarkan konteks yang diberikan. "
                                "Gunakan bahasa Indonesia dan format Markdown yang rapi."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.2,
                    max_tokens=1024,
                ),
                timeout=30.0,
            )

            answer = response.choices[0].message.content
            if not answer:
                raise HTTPException(status_code=503, detail="Respons kosong dari Groq API.")

            return answer.strip()
        except asyncio.TimeoutError:
            raise HTTPException(status_code=503, detail="Groq API tidak merespons dalam 30 detik.")
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(status_code=503, detail=f"Terjadi error saat memanggil Groq API: {error}")

    async def generate_qwen_answer(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {settings.HF_API_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Anda adalah chatbot IT Support. "
                            "Jawab hanya berdasarkan konteks yang diberikan. "
                            "Gunakan bahasa Indonesia dan format Markdown yang rapi."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 1024,
            }

            response = await asyncio.wait_for(
                asyncio.to_thread(
                    requests.post,
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=60,
                ),
                timeout=60,
            )

            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            return answer.strip()
        except asyncio.TimeoutError:
            raise HTTPException(status_code=503, detail="Qwen API timeout.")
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(status_code=503, detail=f"Qwen API error: {error}")

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
        context = re.sub(r"\s(?=\d+\.\s)", "\n", context)
        context = re.sub(r"[ \t]+", " ", context)
        context = re.sub(r"\n+", "\n", context)

        return context[:1500].strip()

    def generate_mock_answer(self, prompt: str) -> str:
        context = self.extract_context_from_prompt(prompt)
        cleaned_context = self.clean_mock_context(context)

        return (
            "**Mode mock aktif**\n\n"
            "Jawaban berikut diambil dari hasil retrieval knowledge base:\n\n"
            f"{cleaned_context}\n\n"
            "_Catatan: Mode ini tidak menggunakan API LLM, sehingga tidak mengurangi kuota model._"
        )

