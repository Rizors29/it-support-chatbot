import asyncio
import requests

from fastapi import HTTPException

from app.config import settings


class QwenService:
    def __init__(self):
        if not settings.HF_API_KEY:
            raise RuntimeError("HF_API_KEY belum diisi di file .env")

        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.model = settings.HF_MODEL

    async def generate_answer(self, prompt: str) -> str:
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
                    {
                        "role": "user",
                        "content": prompt,
                    },
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
            raise HTTPException(
                status_code=503,
                detail="Qwen API timeout.",
            )

        except Exception as error:
            raise HTTPException(
                status_code=503,
                detail=f"Qwen API error: {str(error)}",
            )