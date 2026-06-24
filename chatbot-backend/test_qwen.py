import requests
from app.config import settings

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {settings.HF_API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "messages": [
        {
            "role": "user",
            "content": "Halo, siapa kamu?"
        }
    ],
    "model": settings.HF_MODEL
}

response = requests.post(
    API_URL,
    headers=headers,
    json=payload,
)

print(response.status_code)
print(response.text)