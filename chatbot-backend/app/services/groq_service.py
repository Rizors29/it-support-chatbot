import asyncio

from fastapi import HTTPException
from groq import Groq

from app.config import settings


class GroqService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY belum diisi di file .env")

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_answer(self, prompt: str) -> str:
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
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.2,
                    max_tokens=1024,
                ),
                timeout=30.0,
            )

            answer = response.choices[0].message.content

            if not answer:
                raise HTTPException(
                    status_code=503,
                    detail="Respons kosong dari Groq API.",
                )

            return answer.strip()

        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=503,
                detail="Groq API tidak merespons dalam 30 detik.",
            )

        except HTTPException:
            raise

        except Exception as error:
            raise HTTPException(
                status_code=503,
                detail=f"Terjadi error saat memanggil Groq API: {str(error)}",
            )