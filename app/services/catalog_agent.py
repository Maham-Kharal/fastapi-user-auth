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
        content_text = (message.get("content") or "").strip()
        tool_calls = message.get("tool_calls")
        if not tool_calls:
            if "high traffic" in content_text.lower() or "experiencing high traffic" in content_text.lower() or not content_text:
                if "borrow" in request.lower() or "my books" in request.lower():
                    res_data = execute_tool("get_my_borrowed_books", {}, user_id, db)
                else:
                    res_data = execute_tool("search_books", {"query": request}, user_id, db)

                if isinstance(res_data, dict) and "results" in res_data:
                    books = res_data["results"]
                    if isinstance(books, list) and books:
                        b_str = "\n".join([f"• '{b.get('title')}' by {b.get('author')} (Available: {b.get('available_copies')}/{b.get('total_copies')})" for b in books])
                        return f"Based on our library catalog records:\n{b_str}"
                    elif isinstance(books, list) and not books:
                        return f"I searched our library catalog for '{request}', but didn't find matching titles currently listed."
                return f"I checked our library catalog for '{request}'."
            return content_text

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