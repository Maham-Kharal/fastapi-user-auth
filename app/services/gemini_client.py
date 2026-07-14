import json
import httpx
from fastapi import HTTPException
from app.core.config import settings

GEMINI_MODEL = "gemini-3.5-flash"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}"

INPUT_COST_PER_MILLION = 0.30
OUTPUT_COST_PER_MILLION = 2.50

SYSTEM_PROMPT = (
    "You are a friendly assistant for 'Sweet Crumbs Bakery', a cake and pastry shop. "
    "Help customers with cake flavors, sizes, pricing questions, custom orders, "
    "allergy/ingredient questions, and delivery or pickup info. "
    "If you don't know a specific real detail, say so honestly instead of making it up. "
    "Keep replies warm, concise, and helpful."
)


def _build_contents(history: list[dict]) -> list[dict]:
    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    return contents


async def ask_gemini(history: list[dict]) -> dict:
    url = f"{BASE_URL}:generateContent"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": _build_contents(history),
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512},
    }
    params = {"key": settings.GEMINI_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        raise HTTPException(504, "AI service timed out. Try again.")
    except httpx.HTTPStatusError:
        raise HTTPException(502, "AI service error. Try again.")

    reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
    usage = data.get("usageMetadata", {})
    prompt_tokens = usage.get("promptTokenCount", 0)
    completion_tokens = usage.get("candidatesTokenCount", 0)
    cost = (prompt_tokens / 1_000_000) * INPUT_COST_PER_MILLION + (completion_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION

    return {
        "reply": reply_text,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost_usd": round(cost, 6),
    }
async def stream_gemini(history: list[dict]):
    """Yields reply text chunks as Gemini generates them."""
    url = f"{BASE_URL}:streamGenerateContent"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": _build_contents(history),
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 512,
            "thinkingConfig": {"thinkingBudget": 0},  # disable thinking — faster, cheaper, simpler parsing
        },
    }
    params = {"key": settings.GEMINI_API_KEY, "alt": "sse"}

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", url, params=params, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                chunk_data = line[len("data: "):]
                try:
                    parsed = json.loads(chunk_data)
                    candidates = parsed.get("candidates", [])
                    if not candidates:
                        continue
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        if part.get("thought"):
                            continue  # skip hidden reasoning steps
                        text = part.get("text")
                        if text:
                            yield text
                except json.JSONDecodeError:
                    continue

