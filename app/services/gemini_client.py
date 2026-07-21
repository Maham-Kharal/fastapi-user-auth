import json
import asyncio
import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.services.tool_definitions import LIBRARY_TOOLS
from app.services.tool_dispatcher import execute_tool
from app.services.qdrant_service import search_library

GEMINI_MODEL = "gemini-2.0-flash"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}"

INPUT_COST_PER_MILLION = 0.30
OUTPUT_COST_PER_MILLION = 2.50

SYSTEM_PROMPT = (
    "You are the Library Book Assistant — a friendly, helpful librarian for our library system. "
    "Your role is to help users search for books, check availability, borrow books, return books, "
    "and view their currently borrowed books. "
    "Speak warmly and helpfully, like a real librarian who loves books. "
    "Only help with library-related requests — if someone asks about anything unrelated to the "
    "library (books, borrowing, availability, returns), politely decline and steer the conversation "
    "back to how you can help with the library. "
    "IMPORTANT: Never guess or make up information about books, availability, or loans. "
    "Always use the appropriate tool to look up real data before answering — even if you think "
    "you already know the answer."
)


def _build_contents(history: list[dict]) -> list[dict]:
    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    return contents


def _extract_knowledge_fallback(system_prompt_override: str) -> str:
    """If Gemini API hits 429 rate limits, extract answer directly from Qdrant retrieved context."""
    if system_prompt_override and "Relevant library knowledge retrieved from database:" in system_prompt_override:
        try:
            parts = system_prompt_override.split("Relevant library knowledge retrieved from database:\n")
            knowledge = parts[1].split("\nUse this information")[0].strip()
            lines = [l.strip("- ") for l in knowledge.split("\n") if l.strip()]
            if lines:
                return "Based on our library records:\n" + "\n".join(f"• {l}" for l in lines)
        except Exception:
            pass
    return "The library AI is experiencing high traffic right now. Please try asking again in a moment."


async def ask_gemini(history: list[dict]) -> dict:
    """Non-tool-calling version — still used by your bakery-style /chat routes if needed."""
    url = f"{BASE_URL}:generateContent"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": _build_contents(history),
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512},
    }
    params = {"key": settings.GEMINI_API_KEY}

    MAX_RETRIES = 5
    retry_delay = 3.0
    data = None

    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, params=params, json=payload)
                if response.status_code in (429, 503):
                    if attempt < MAX_RETRIES - 1:
                        print(f"Gemini API returned {response.status_code} (Rate Limit). Retrying in {retry_delay}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                response.raise_for_status()
                data = response.json()
                break
        except httpx.TimeoutException:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
                continue
            return {"reply": "Sorry, the request timed out. Please try again.", "raw": None}
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (429, 503) and attempt < MAX_RETRIES - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
                continue
            print(f"Gemini HTTPStatusError: {e}")
            return {"reply": "", "raw": None}
        except Exception as e:
            print(f"Gemini unexpected error: {e}")
            return {"reply": "", "raw": None}

    if data is None:
        return {"reply": "", "raw": None}

    # Extract and return reply text
    try:
        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        reply_text = ""

    return {"reply": reply_text, "raw": data}

async def stream_gemini(history: list[dict], system_prompt_override: str = None):
    """Yields reply text chunks as Gemini generates them. Used by the HTTP SSE chat routes."""
    url = f"{BASE_URL}:streamGenerateContent"
    system_prompt = system_prompt_override if system_prompt_override is not None else SYSTEM_PROMPT
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": _build_contents(history),
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 512,
        },
    }
    params = {"key": settings.GEMINI_API_KEY, "alt": "sse"}

    MAX_RETRIES = 3
    retry_delay = 2.0

    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                async with client.stream("POST", url, params=params, json=payload) as response:
                    if response.status_code in (429, 503):
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        else:
                            yield _extract_knowledge_fallback(system_prompt_override)
                            return

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
                                    continue
                                text = part.get("text")
                                if text:
                                    yield text
                        except json.JSONDecodeError:
                            continue
                    return  # stream finished successfully

        except Exception as e:
            print(f"Streaming attempt {attempt+1} error: {e}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
                continue

    # Fallback to direct context extraction if Gemini API is unavailable/rate-limited
    yield _extract_knowledge_fallback(system_prompt_override)


async def ask_gemini_with_tools(history: list[dict], user_id: int, db) -> dict:
    """
    The tool-calling loop:
    1. Retrieve relevant context from Qdrant (RAG) using the latest user message
    2. Send message + tool menu + RAG context to Gemini
    3. If Gemini wants a tool, run the REAL Python function (execute_tool)
    4. Send the real result back to Gemini
    5. Repeat until Gemini gives a final text answer (or we hit a safety limit)
    """
    url = f"{BASE_URL}:generateContent"
    contents = _build_contents(history)

    # ── RAG: Retrieve relevant library context from Qdrant ────────────────────
    # Use the most recent user message as the search query
    last_user_message = ""
    for msg in reversed(history):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break

    rag_context_parts = []
    if last_user_message:
        rag_context_parts = await search_library(last_user_message, top_k=3)

    # Build the system prompt — append RAG context if we found anything
    system_prompt = SYSTEM_PROMPT
    if rag_context_parts:
        context_block = "\n".join(f"- {c}" for c in rag_context_parts)
        system_prompt = (
            system_prompt
            + "\n\nRelevant library knowledge retrieved from database:\n"
            + context_block
            + "\nUse this information to give accurate, grounded answers."
        )
    # ─────────────────────────────────────────────────────────────────────────

    total_prompt_tokens = 0
    total_completion_tokens = 0
    MAX_TOOL_LOOPS = 5  # safety limit — stop if Gemini somehow loops forever

    for _ in range(MAX_TOOL_LOOPS):
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "tools": LIBRARY_TOOLS,
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512},
        }
        params = {"key": settings.GEMINI_API_KEY}

        import asyncio
        MAX_RETRIES = 3
        retry_delay = 2.0
        data = None

        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(url, params=params, json=payload)
                    if response.status_code in (429, 503):
                        if attempt < MAX_RETRIES - 1:
                            print(f"Gemini API returned status {response.status_code}. Retrying in {retry_delay}s... (Attempt {attempt+1}/{MAX_RETRIES})")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                    if response.status_code == 400:
                        print("GEMINI 400 ERROR BODY:", response.text)
                    response.raise_for_status()
                    data = response.json()
                    break
            except httpx.TimeoutException:
                if attempt < MAX_RETRIES - 1:
                    print(f"Gemini API request timed out. Retrying in {retry_delay}s... (Attempt {attempt+1}/{MAX_RETRIES})")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return {"reply": "Sorry, the library assistant is taking too long to respond. Please try again.", "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0}
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 503):
                    if attempt < MAX_RETRIES - 1:
                        print(f"Gemini API returned status {e.response.status_code}. Retrying in {retry_delay}s... (Attempt {attempt+1}/{MAX_RETRIES})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                return {"reply": f"Sorry, something went wrong reaching the library assistant. Details: {e.response.text}", "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0}

        if data is None:
            return {"reply": "We're getting a lot of requests right now! Please wait a moment and try again.", "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0}

        usage = data.get("usageMetadata", {})
        total_prompt_tokens += usage.get("promptTokenCount", 0)
        total_completion_tokens += usage.get("candidatesTokenCount", 0)

        candidate = data["candidates"][0]
        parts = candidate["content"]["parts"]

        function_call_part = None
        for part in parts:
            if "functionCall" in part:
                function_call_part = part["functionCall"]
                break

        if function_call_part is None:
            # No tool call — Gemini is giving its final answer
            reply_text = "".join(p.get("text", "") for p in parts)
            cost = (total_prompt_tokens / 1_000_000) * INPUT_COST_PER_MILLION + (total_completion_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION
            return {
                "reply": reply_text,
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "cost_usd": round(cost, 6),
            }

        # Gemini wants a tool — run the REAL function
        tool_name = function_call_part["name"]
        tool_args = function_call_part.get("args", {})

        contents.append({"role": "model", "parts": parts})

        result = execute_tool(tool_name, tool_args, user_id, db)

        contents.append({
            "role": "user",
            "parts": [{"functionResponse": {"name": tool_name, "response": result}}],
        })
        # loop continues — Gemini now sees the real result and decides what to do next

    raise HTTPException(500, "Assistant made too many tool calls in a row — please try again.")