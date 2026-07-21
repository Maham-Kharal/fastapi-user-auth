import json
import asyncio
from app.services.cerebras_client import call_cerebras
from app.services.qdrant_service import search_library
from langfuse import observe

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


@observe(name="policy-agent")
async def run_policy_agent(request: str) -> str:
    print("===== POLICY AGENT =====")
    print("Request:", request)
    
    # Maintain standard messages list for OpenAI chat completion format
    messages = [{"role": "user", "content": request}]
    MAX_TOOL_LOOPS = 5

    for _ in range(MAX_TOOL_LOOPS):
        res = await call_cerebras(
            messages=messages,
            tools=POLICY_TOOLS,
            system_prompt=POLICY_SYSTEM_PROMPT,
            temperature=0.2
        )
        
        choices = res.get("choices", [])
        if not choices:
            return "Sorry, I couldn't get a response from the policy service."
            
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
            result = await _execute_policy_tool(name, args)
            
            # Append tool execution result
            messages.append({
                "role": "tool",
                "tool_call_id": tc_id,
                "name": name,
                "content": json.dumps(result) if not isinstance(result, str) else result
            })

    return "I wasn't able to finish that policy lookup — please try rephrasing."