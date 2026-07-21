import asyncio
import httpx
from app.core.config import settings
from app.services.gemini_client import BASE_URL
from app.services.catalog_agent import run_catalog_agent
from app.services.policy_agent import run_policy_agent

ORCHESTRATOR_TOOLS = [{
    "function_declarations": [
        {
            "name": "call_catalog_agent",
            "description": "Route to the Catalog Agent — for searching books, checking availability, borrowing, returning, or listing a user's borrowed books.",
            "parameters": {
                "type": "object",
                "properties": {"request": {"type": "string", "description": "The user's request, rephrased if needed"}},
                "required": ["request"],
            },
        },
        {
            "name": "call_policy_agent",
            "description": "Route to the Policy Agent — for questions about library hours, borrowing rules, fines, membership, or other policies.",
            "parameters": {
                "type": "object",
                "properties": {"request": {"type": "string", "description": "The user's request, rephrased if needed"}},
                "required": ["request"],
            },
        },
    ]
}]

ORCHESTRATOR_SYSTEM_PROMPT = (
    "You are the Orchestrator for a library assistant. You do NOT answer questions yourself "
    "and you know no library data. Your only job is routing:\n"
    "- call_catalog_agent: searching books, availability, borrowing, returning, borrowed-books list.\n"
    "- call_policy_agent: hours, borrowing limits, fines, membership, other policies.\n"
    "If a request needs both, call both agents in the same turn. Once you have the needed "
    "agent response(s), combine them into one warm final answer. Never mention 'Catalog Agent', "
    "'Policy Agent', 'orchestrator', or 'routing' in your final answer."
)

MAX_HOPS = 4  # guardrail — max routing round-trips before forcing a final answer

async def orchestrate(user_message: str, user_id: int, db) -> str:
    print("===== ORCHESTRATOR START =====")
    print("User message:", user_message)

    url = f"{BASE_URL}:generateContent"
    contents = [{"role": "user", "parts": [{"text": user_message}]}]

    MAX_RETRIES = 3

    for _ in range(MAX_HOPS):
        payload = {
            "system_instruction": {"parts": [{"text": ORCHESTRATOR_SYSTEM_PROMPT}]},
            "contents": contents,
            "tools": ORCHESTRATOR_TOOLS,
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 512},
        }
        params = {"key": settings.GEMINI_API_KEY}
        retry_delay = 2.0
        data = None

        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(url, params=params, json=payload)

                    print("Gemini response status:", response.status_code)

                    if response.status_code in (429, 503) and attempt < MAX_RETRIES - 1:

                        await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                    response.raise_for_status()
                    data = response.json()
                    break
            except httpx.TimeoutException:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                return "Sorry, the assistant is taking too long to respond. Please try again."
            except httpx.HTTPStatusError:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(retry_delay); retry_delay *= 2; continue
                return "Sorry, something went wrong. Please try again."

        if data is None:
            return "We're getting a lot of requests right now! Please wait a moment and try again."

        parts = data["candidates"][0]["content"]["parts"]
        calls = [p["functionCall"] for p in parts if "functionCall" in p]

        if not calls:
            return "".join(p.get("text", "") for p in parts).strip()

        contents.append({"role": "model", "parts": parts})

        for fc in calls:
            name = fc["name"]
            request_text = fc.get("args", {}).get("request", user_message)
            if name == "call_catalog_agent":
                reply = await run_catalog_agent(request_text, user_id, db)
            elif name == "call_policy_agent":
                reply = await run_policy_agent(request_text)
            else:
                reply = f"Unknown agent: {name}"

            contents.append({
                "role": "user",
                "parts": [{"functionResponse": {"name": name, "response": {"answer": reply}}}],
            })
        # loop continues — orchestrator sees agent replies, can respond or route again

    return "That needed more back-and-forth than I could complete — could you try rephrasing or splitting it into two questions?"