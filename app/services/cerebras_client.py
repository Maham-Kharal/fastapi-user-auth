import json
import httpx
from fastapi import HTTPException
from app.core.config import settings
from langfuse import get_client, observe

CEREBRAS_URL = "https://api.cerebras.ai/v1/chat/completions"

def get_openai_tools(gemini_tools: list) -> list:
    """
    Converts Gemini-style tool declarations to OpenAI-style tools.
    Gemini format: [{"function_declarations": [{"name": ..., "description": ..., "parameters": ...}]}]
    OpenAI format: [{"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}]
    """
    if not gemini_tools:
        return None
    
    openai_tools = []
    for tool_group in gemini_tools:
        if "function_declarations" in tool_group:
            for fd in tool_group["function_declarations"]:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": fd["name"],
                        "description": fd["description"],
                        "parameters": fd["parameters"]
                    }
                })
    return openai_tools if openai_tools else None


async def call_gemini_fallback(
    messages: list[dict],
    tools: list = None,
    system_prompt: str = None,
    temperature: float = 0.2
) -> dict:
    """
    Fallback to Gemini 2.0 Flash REST API if Cerebras is unavailable (e.g. 402 Payment Required).
    Translates OpenAI-style messages & tools to Gemini format, and converts output back to OpenAI choice schema.
    """
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Neither Cerebras nor Gemini API keys are available.")

    candidate_models = ["models/gemini-flash-latest", "models/gemini-3.6-flash", "models/gemini-2.0-flash"]

    payload = {
        "generationConfig": {"temperature": temperature}
    }

    if system_prompt:
        payload["system_instruction"] = {"parts": [{"text": system_prompt}]}

    # Build Gemini tools
    if tools:
        gemini_fd = []
        for t in tools:
            if "function_declarations" in t:
                gemini_fd.extend(t["function_declarations"])
            elif t.get("type") == "function" and "function" in t:
                gemini_fd.append(t["function"])
        if gemini_fd:
            payload["tools"] = [{"function_declarations": gemini_fd}]

    # Build Gemini contents from messages
    gemini_contents = []
    for msg in messages:
        role = msg.get("role")
        if role == "system":
            continue

        g_role = "model" if role in ("assistant", "model") else "user"
        parts = []

        if "content" in msg and msg["content"]:
            parts.append({"text": str(msg["content"])})

        if "tool_calls" in msg and msg["tool_calls"]:
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {})
                args_str = fn.get("arguments", "{}")
                try:
                    args_obj = json.loads(args_str) if isinstance(args_str, str) else args_str
                except Exception:
                    args_obj = {}
                parts.append({"functionCall": {"name": fn.get("name"), "args": args_obj}})

        if role == "tool":
            content_val = msg.get("content", "")
            try:
                resp_obj = json.loads(content_val) if isinstance(content_val, str) else {"result": content_val}
            except Exception:
                resp_obj = {"result": content_val}
            parts.append({
                "functionResponse": {
                    "name": msg.get("name", "tool"),
                    "response": resp_obj
                }
            })

        if parts:
            gemini_contents.append({"role": g_role, "parts": parts})

    payload["contents"] = gemini_contents if gemini_contents else [{"role": "user", "parts": [{"text": "Hello"}]}]

    import asyncio
    data = None

    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        backoff = 2.0
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=25.0) as client:
                    response = await client.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        break
                    elif response.status_code in (429, 503):
                        await asyncio.sleep(backoff)
                        backoff *= 2.0
                        continue
            except Exception as e:
                print(f"[Gemini Fallback] Model {model_name} attempt {attempt+1} failed: {e}")
                await asyncio.sleep(backoff)
                backoff *= 2.0
        if data:
            break


    if not data:
        return {
            "choices": [{"message": {"role": "assistant", "content": "The library assistant is experiencing high traffic. Please try again in a moment."}}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0}
        }

    candidates = data.get("candidates", []) if data else []
    if not candidates:
        return {
            "choices": [{"message": {"role": "assistant", "content": "No response generated."}}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0}
        }

    first_cand = candidates[0]
    content_parts = first_cand.get("content", {}).get("parts", [])

    text_pieces = []
    tool_calls = []
    for idx, part in enumerate(content_parts):
        if "text" in part:
            text_pieces.append(part["text"])
        if "functionCall" in part:
            fc = part["functionCall"]
            tool_calls.append({
                "id": f"call_gemini_{idx}",
                "type": "function",
                "function": {
                    "name": fc["name"],
                    "arguments": json.dumps(fc.get("args", {}))
                }
            })

    msg_dict = {"role": "assistant"}
    msg_dict["content"] = "\n".join(text_pieces) if text_pieces else None
    if tool_calls:
        msg_dict["tool_calls"] = tool_calls

    usage = data.get("usageMetadata", {})
    return {
        "choices": [{"message": msg_dict}],
        "usage": {
            "prompt_tokens": usage.get("promptTokenCount", 0),
            "completion_tokens": usage.get("candidatesTokenCount", 0)
        }
    }


_cerebras_disabled = False

async def call_cerebras(
    messages: list[dict], 
    tools: list = None, 
    system_prompt: str = None,
    temperature: float = 0.2
) -> dict:
    """
    Call Cerebras API using OpenAI-compatible chat completions.
    Falls back to Gemini 2.0 Flash if Cerebras fails (e.g. 402 Payment Required or 429 Rate Limit).
    """
    global _cerebras_disabled

    if settings.CEREBRAS_API_KEY and not _cerebras_disabled:
        headers = {
            "Authorization": f"Bearer {settings.CEREBRAS_API_KEY}",
            "Content-Type": "application/json",
        }

        # Format messages: prepend system prompt if present
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        
        for msg in messages:
            role = msg["role"]
            if role == "model":
                role = "assistant"
            
            formatted_msg = {"role": role}
            if "content" in msg and msg["content"] is not None:
                formatted_msg["content"] = msg["content"]
            
            if "tool_calls" in msg:
                formatted_msg["tool_calls"] = msg["tool_calls"]
            if "tool_call_id" in msg:
                formatted_msg["tool_call_id"] = msg["tool_call_id"]
            if "name" in msg:
                formatted_msg["name"] = msg["name"]
                
            formatted_messages.append(formatted_msg)

        openai_tools = get_openai_tools(tools) if tools else None

        payload = {
            "model": settings.CEREBRAS_MODEL,
            "messages": formatted_messages,
            "temperature": temperature,
        }
        if openai_tools:
            payload["tools"] = openai_tools

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(CEREBRAS_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            # Record Langfuse observation if successful
            try:
                langfuse = get_client()
                with langfuse.start_as_current_observation(
                    as_type="generation",
                    name="cerebras-completion",
                    model=settings.CEREBRAS_MODEL,
                    input=formatted_messages
                ) as generation:
                    choices = data.get("choices", [])
                    usage = data.get("usage", {})
                    if choices:
                        message_content = choices[0].get("message", {}).get("content", "")
                        tool_calls = choices[0].get("message", {}).get("tool_calls", None)
                        generation.update(
                            output={"content": message_content, "tool_calls": tool_calls},
                            usage_details={"input_tokens": usage.get("prompt_tokens", 0), "output_tokens": usage.get("completion_tokens", 0)}
                        )
            except Exception:
                pass

            return data
        except Exception as e:
            _cerebras_disabled = True
            print(f"[LLM Client] Cerebras API failed ({e}). Disabling Cerebras for session & falling back to Gemini...")

    # Fallback to Gemini if Cerebras key missing/disabled or Cerebras request failed
    return await call_gemini_fallback(messages, tools, system_prompt, temperature)


