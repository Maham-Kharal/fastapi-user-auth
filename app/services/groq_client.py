import httpx
from app.core.config import settings


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


async def call_groq(messages, tools=None):

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.3,
    }

    if tools:
        payload["tools"] = tools

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_URL,
            headers=headers,
            json=payload
        )

        response.raise_for_status()

        return response.json()
