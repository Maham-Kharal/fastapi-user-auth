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


async def call_cerebras(
    messages: list[dict], 
    tools: list = None, 
    system_prompt: str = None,
    temperature: float = 0.2
) -> dict:
    """
    Call Cerebras API using OpenAI-compatible chat completions.
    Traced manually as a "generation" using Langfuse get_client() to support SDK v3/v4.
    """
    if not settings.CEREBRAS_API_KEY:
        raise HTTPException(status_code=500, detail="Cerebras API key not configured.")

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

    # Get Langfuse client and start tracing this specific generation
    langfuse = get_client()
    
    with langfuse.start_as_current_observation(
        as_type="generation",
        name="cerebras-completion",
        model=settings.CEREBRAS_MODEL,
        input=formatted_messages
    ) as generation:
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(CEREBRAS_URL, headers=headers, json=payload)
            if response.status_code == 429:
                print("Cerebras API Rate Limit (429).")
            response.raise_for_status()
            data = response.json()

        choices = data.get("choices", [])
        usage = data.get("usage", {})
        
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        # Update Langfuse observation
        if choices:
            message_content = choices[0].get("message", {}).get("content", "")
            tool_calls = choices[0].get("message", {}).get("tool_calls", None)
            output_log = {"content": message_content}
            if tool_calls:
                output_log["tool_calls"] = tool_calls
            
            generation.update(
                output=output_log,
                usage_details={
                    "input_tokens": prompt_tokens,
                    "output_tokens": completion_tokens
                }
            )

        return data
