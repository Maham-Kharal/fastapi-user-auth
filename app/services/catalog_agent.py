import json
import asyncio
from app.services.cerebras_client import call_cerebras
from app.services.tool_definitions import LIBRARY_TOOLS
from app.services.tool_dispatcher import execute_tool
from langfuse import observe

CATALOG_TOOLS = LIBRARY_TOOLS  # already just the 5 catalog tools

CATALOG_SYSTEM_PROMPT = (
    "You are the Catalog Agent for a library system. You handle searching for books, "
    "checking availability, borrowing, returning, and listing a user's borrowed books. "
    "Always use the provided tools to look up real data — never guess. "
    "Give a warm, concise, factual answer once you have the tool results."
)


@observe(name="catalog-agent")
async def run_catalog_agent(request: str, user_id: int, db) -> str:
    print("===== CATALOG AGENT =====")
    print("Request:", request)
    
    # Maintain standard messages list for OpenAI chat completion format
    messages = [{"role": "user", "content": request}]
    MAX_TOOL_LOOPS = 5

    for _ in range(MAX_TOOL_LOOPS):
        res = await call_cerebras(
            messages=messages,
            tools=CATALOG_TOOLS,
            system_prompt=CATALOG_SYSTEM_PROMPT,
            temperature=0.2
        )
        
        choices = res.get("choices", [])
        if not choices:
            return "Sorry, I couldn't get a response from the catalog service."
            
        message = choices[0].get("message", {})
        
        # Append the assistant message (which might contain tool_calls)
        messages.append({
            "role": "assistant",
            "content": message.get("content"),
            "tool_calls": message.get("tool_calls")
        })

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            # If no tool calls, return final reply
            return message.get("content", "").strip()

        # Handle all tool calls requested in this turn
        for tc in tool_calls:
            tc_id = tc.get("id")
            fn = tc.get("function", {})
            name = fn.get("name")
            args_str = fn.get("arguments", "{}")
            
            try:
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
            except Exception:
                args = {}

            # Execute tool logic
            result = execute_tool(name, args, user_id, db)
            
            # Append tool execution result
            messages.append({
                "role": "tool",
                "tool_call_id": tc_id,
                "name": name,
                "content": json.dumps(result) if not isinstance(result, str) else result
            })

    return "I wasn't able to finish that catalog request — please try rephrasing."