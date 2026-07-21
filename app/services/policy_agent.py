import asyncio
import httpx
from app.core.config import settings
from app.services.gemini_client import BASE_URL
from app.services.qdrant_service import search_library

POLICY_TOOLS = [{
    "function_declarations": [{
        "name": "search_knowledge_base",
        "description": "Search the library's policy knowledge base (hours, borrowing rules, fines, membership, etc.)",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "The policy question or topic to search for"}},
            "required": ["query"],
        },
    }]
}]

POLICY_SYSTEM_PROMPT = (
    "You are the Policy Agent for a library system. You answer questions about library "
    "hours, borrowing limits, fines, membership, and other policies. Always use the "
    "search_knowledge_base tool to look up real policy text before answering — never guess. "
    "Give a warm, concise, factual answer grounded only in what the tool returns."
)


async def _execute_policy_tool(name: str, args: dict) -> dict:
    

    if name == "search_knowledge_base":
        results = await search_library(args.get("query", ""), top_k=3)
        return {"results": results}
    return {"error": f"Unknown tool: {name}"}


async def run_policy_agent(request: str) -> str:
    print("===== POLICY AGENT =====")
    print("Request:", request)
    url = f"{BASE_URL}:generateContent"
    contents = [{"role": "user", "parts": [{"text": request}]}]
    MAX_TOOL_LOOPS = 4
    MAX_RETRIES = 3

    for _ in range(MAX_TOOL_LOOPS):
        payload = {
            "system_instruction": {"parts": [{"text": POLICY_SYSTEM_PROMPT}]},
            "contents": contents,
            "tools": POLICY_TOOLS,
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
                return "Sorry, the policy lookup is taking too long. Please try again."
            except httpx.HTTPStatusError:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                return "Sorry, I couldn't reach the policy knowledge base right now."

        if data is None:
            return "The policy system is busy right now. Please try again shortly."

        parts = data["candidates"][0]["content"]["parts"]
        fc = next((p["functionCall"] for p in parts if "functionCall" in p), None)

        if fc is None:
            return "".join(p.get("text", "") for p in parts).strip()

        contents.append({"role": "model", "parts": parts})
        result = await _execute_policy_tool(fc["name"], fc.get("args", {}))
        contents.append({"role": "user", "parts": [{"functionResponse": {"name": fc["name"], "response": result}}]})

    return "I wasn't able to finish that policy lookup — please try rephrasing."