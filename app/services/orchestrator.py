import json
import asyncio
from app.services.cerebras_client import call_cerebras
from app.services.catalog_agent import run_catalog_agent
from app.services.policy_agent import run_policy_agent
from langfuse import observe

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
            "description": "Route to the Policy Agent — for questions about library hours, borrowing limits, fines, membership, or other policies.",
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


@observe(name="orchestrator")
async def run_orchestrator(user_message: str, user_id: int, db) -> str:
    print("===== ORCHESTRATOR START =====")
    print("User message:", user_message)

    messages = [{"role": "user", "content": user_message}]
    MAX_HOPS = 4

    for hop in range(MAX_HOPS):
        res = await call_cerebras(
            messages=messages,
            tools=ORCHESTRATOR_TOOLS,
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            temperature=0.2
        )
        
        choices = res.get("choices", [])
        if not choices:
            return "Sorry, I couldn't orchestrate a response."
            
        message = choices[0].get("message", {})
        
        # Append the assistant message (which might contain tool_calls)
        messages.append({
            "role": "assistant",
            "content": message.get("content"),
            "tool_calls": message.get("tool_calls")
        })

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            content_text = message.get("content", "").strip()
            if "high traffic" in content_text.lower() or "experiencing high traffic" in content_text.lower() or not content_text:
                um_lower = user_message.lower()
                if any(w in um_lower for w in ["book", "borrow", "author", "title", "read", "harry potter", "dune", "hobbit", "moby", "search"]):
                    return await run_catalog_agent(user_message, user_id, db)
                else:
                    return await run_policy_agent(user_message)
            return content_text


        # Handle routing to specialists
        for tc in tool_calls:
            tc_id = tc.get("id")
            fn = tc.get("function", {})
            name = fn.get("name")
            args_str = fn.get("arguments", "{}")
            
            try:
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
            except Exception:
                args = {}

            request_text = args.get("request", user_message)
            
            if name == "call_catalog_agent":
                reply = await run_catalog_agent(request_text, user_id, db)
            elif name == "call_policy_agent":
                reply = await run_policy_agent(request_text)
            else:
                reply = f"Unknown agent: {name}"

            # Append the agent response as tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tc_id,
                "name": name,
                "content": json.dumps({"answer": reply})
            })

    return "That needed more back-and-forth than I could complete — could you try rephrasing or splitting it into two questions?"

# Alias for backwards compatibility with endpoints importing `orchestrate`
orchestrate = run_orchestrator