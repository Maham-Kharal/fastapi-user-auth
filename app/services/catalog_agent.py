import asyncio
import httpx
from app.core.config import settings
from app.services.gemini_client import BASE_URL
from app.services.tool_definitions import LIBRARY_TOOLS
from app.services.tool_dispatcher import execute_tool

CATALOG_TOOLS = LIBRARY_TOOLS  # already just the 5 catalog tools

CATALOG_SYSTEM_PROMPT = (
    "You are the Catalog Agent for a library system. You handle searching for books, "
    "checking availability, borrowing, returning, and listing a user's borrowed books. "
    "Always use the provided tools to look up real data — never guess. "
    "Give a warm, concise, factual answer once you have the tool results."
)


async def run_catalog_agent(request: str, user_id: int, db) -> str:
    print("===== CATALOG AGENT =====")
    print("Request:", request)
    url = f"{BASE_URL}:generateContent"
    contents = [{"role": "user", "parts": [{"text": request}]}]
    MAX_TOOL_LOOPS = 4
    MAX_RETRIES = 3

    for _ in range(MAX_TOOL_LOOPS):
        payload = {
            "system_instruction": {"parts": [{"text": CATALOG_SYSTEM_PROMPT}]},
            "contents": contents,
            "tools": CATALOG_TOOLS,
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 512},
        }
        params = {"key": settings.GEMINI_API_KEY}
        retry_delay = 2.0
        data = None

        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(url, params=params, json=payload)
                    if response.status_code in (429, 503) and attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                    response.raise_for_status()
                    data = response.json()
                    break
            except httpx.TimeoutException:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                return "Sorry, the catalog lookup is taking too long. Please try again."
            except httpx.HTTPStatusError:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                return "Sorry, I couldn't reach the catalog system right now."

        if data is None:
            return "The catalog system is busy right now. Please try again shortly."

        parts = data["candidates"][0]["content"]["parts"]
        fc = next((p["functionCall"] for p in parts if "functionCall" in p), None)

        if fc is None:
            return "".join(p.get("text", "") for p in parts).strip()

        contents.append({"role": "model", "parts": parts})
        result = execute_tool(fc["name"], fc.get("args", {}), user_id, db)
        contents.append({"role": "user", "parts": [{"functionResponse": {"name": fc["name"], "response": result}}]})

    return "I wasn't able to finish that catalog request — please try rephrasing."