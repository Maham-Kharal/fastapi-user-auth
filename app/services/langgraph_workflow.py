import os
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.services.tool_dispatcher import execute_tool
from app.services.qdrant_service import search_library

class MessagesState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: int
    db: any  # We pass db in state for simplicity (it won't be serialized to DB anyway since we aren't using checkpointing here)
    route: str # To keep track of where to go

# -----------------------------------------------------------------------------
# LLM Setup (Cerebras via OpenAI interface)
# -----------------------------------------------------------------------------
from app.core.config import settings

llm = ChatOpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=settings.CEREBRAS_API_KEY or "DUMMY_KEY",
    model=settings.CEREBRAS_MODEL,
    temperature=0.2
)

# -----------------------------------------------------------------------------
# Nodes & Routing
# -----------------------------------------------------------------------------

def orchestrator_node(state: MessagesState):
    """
    The orchestrator analyzes the user's message and decides whether to route
    to the catalog agent, the policy agent, or answer directly if it's a greeting.
    """
    prompt = (
        "You are the Orchestrator for a library assistant. Your job is routing.\n"
        "Read the user's message and determine if it requires:\n"
        "1) The Catalog Agent (for searching books, availability, borrowing, returning, borrowed-books list).\n"
        "2) The Policy Agent (for hours, borrowing limits, fines, membership, other policies).\n"
        "If you can answer without tools (like a simple greeting), just answer normally.\n"
        "To route, output a tool call to 'route_to_catalog' or 'route_to_policy'."
    )
    
    # We define dummy tools just for routing
    def route_to_catalog(request: str) -> str:
        """Route to the Catalog Agent."""
        pass
    def route_to_policy(request: str) -> str:
        """Route to the Policy Agent."""
        pass
        
    router_llm = llm.bind_tools([route_to_catalog, route_to_policy])
    
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    response = router_llm.invoke(messages)
    
    # Check if a routing tool was called
    route = "direct"
    if response.tool_calls:
        name = response.tool_calls[0]["name"]
        if name == "route_to_catalog":
            route = "catalog"
        elif name == "route_to_policy":
            route = "policy"
            
    # We don't append the router's internal tool call to the state, 
    # we just use it to set the route flag.
    # Wait, if it didn't route, we return its response.
    if route == "direct":
        return {"messages": [response], "route": route}
    else:
        return {"route": route}

def orchestrator_router(state: MessagesState):
    if state.get("route") == "catalog":
        return "catalog_agent"
    elif state.get("route") == "policy":
        return "policy_agent"
    return END

def catalog_agent_node(state: MessagesState):
    """Catalog agent equipped with DB tools."""
    user_id = state["user_id"]
    db = state["db"]
    
    def search_books_tool(query: str):
        """Search the library catalog for books."""
        return execute_tool("search_books", {"query": query}, user_id, db)
        
    def check_availability_tool(book_id: int):
        """Check if a specific book is currently available to borrow."""
        return execute_tool("check_availability", {"book_id": book_id}, user_id, db)
        
    def borrow_book_tool(book_id: int):
        """Borrow a book from the library."""
        return execute_tool("borrow_book", {"book_id": book_id}, user_id, db)
        
    def return_book_tool(book_id: int):
        """Return a borrowed book to the library."""
        return execute_tool("return_book", {"book_id": book_id}, user_id, db)
        
    def get_borrowed_tool():
        """Get a list of all books currently borrowed by the user."""
        return execute_tool("get_my_borrowed_books", {}, user_id, db)
        
    tools = [
        StructuredTool.from_function(search_books_tool, name="search_books"),
        StructuredTool.from_function(check_availability_tool, name="check_availability"),
        StructuredTool.from_function(borrow_book_tool, name="borrow_book"),
        StructuredTool.from_function(return_book_tool, name="return_book"),
        StructuredTool.from_function(get_borrowed_tool, name="get_my_borrowed_books")
    ]
    
    catalog_llm = llm.bind_tools(tools)
    prompt = "You are the Library Catalog Agent. Use tools to search books, check availability, borrow, and return books."
    
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    
    # We will use a standard LangChain tool loop pattern for the catalog agent itself,
    # OR we can let LangGraph handle tool execution by routing to a ToolNode.
    # For simplicity, we just invoke once. If it calls a tool, we will return the AIMessage with tool_calls,
    # and a conditional edge will route to `catalog_tools`.
    response = catalog_llm.invoke(messages)
    return {"messages": [response]}

def policy_agent_node(state: MessagesState):
    """Policy agent equipped with Qdrant."""
    def search_knowledge_base_tool(query: str):
        """Search the library's policy knowledge base (hours, borrowing rules, fines, membership, etc.)."""
        return search_library(query, top_k=3)
        
    tools = [StructuredTool.from_function(search_knowledge_base_tool, name="search_knowledge_base")]
    policy_llm = llm.bind_tools(tools)
    
    prompt = "You are the Library Policy Agent. Use the search_knowledge_base tool to answer policy questions."
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    
    response = policy_llm.invoke(messages)
    return {"messages": [response]}


# -----------------------------------------------------------------------------
# Tool Execution Node
# -----------------------------------------------------------------------------
import json

def tool_executor_node(state: MessagesState):
    """Executes the tool calls from either agent and appends ToolMessages."""
    last_message = state["messages"][-1]
    user_id = state["user_id"]
    db = state["db"]
    
    tool_messages = []
    for tc in last_message.tool_calls:
        name = tc["name"]
        args = tc["args"]
        tc_id = tc["id"]
        
        try:
            if name == "search_books":
                res = execute_tool("search_books", args, user_id, db)
            elif name == "check_availability":
                res = execute_tool("check_availability", args, user_id, db)
            elif name == "borrow_book":
                res = execute_tool("borrow_book", args, user_id, db)
            elif name == "return_book":
                res = execute_tool("return_book", args, user_id, db)
            elif name == "get_my_borrowed_books":
                res = execute_tool("get_my_borrowed_books", args, user_id, db)
            elif name == "search_knowledge_base":
                res = search_library(args.get("query", ""), top_k=3)
            else:
                res = {"error": f"Unknown tool {name}"}
        except Exception as e:
            res = {"error": str(e)}
            
        tool_messages.append(ToolMessage(content=json.dumps(res), tool_call_id=tc_id))
        
    return {"messages": tool_messages}

def should_continue_catalog(state: MessagesState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "execute_tools"
    return END

def should_continue_policy(state: MessagesState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "execute_tools"
    return END

def route_after_tool(state: MessagesState):
    # Depending on which agent we were in, we route back to it.
    # We can check the route flag we set in orchestrator.
    if state.get("route") == "catalog":
        return "catalog_agent"
    return "policy_agent"

# -----------------------------------------------------------------------------
# Compile Graph
# -----------------------------------------------------------------------------
workflow = StateGraph(MessagesState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("catalog_agent", catalog_agent_node)
workflow.add_node("policy_agent", policy_agent_node)
workflow.add_node("execute_tools", tool_executor_node)

workflow.add_edge(START, "orchestrator")
workflow.add_conditional_edges("orchestrator", orchestrator_router, {
    "catalog_agent": "catalog_agent",
    "policy_agent": "policy_agent",
    END: END
})

workflow.add_conditional_edges("catalog_agent", should_continue_catalog, {
    "execute_tools": "execute_tools",
    END: END
})

workflow.add_conditional_edges("policy_agent", should_continue_policy, {
    "execute_tools": "execute_tools",
    END: END
})

workflow.add_conditional_edges("execute_tools", route_after_tool, {
    "catalog_agent": "catalog_agent",
    "policy_agent": "policy_agent"
})

compiled_graph = workflow.compile()

async def run_langgraph_orchestrator(user_message: str, user_id: int, db) -> str:
    """Entry point to replace the manual orchestrator."""
    inputs = {
        "messages": [HumanMessage(content=user_message)],
        "user_id": user_id,
        "db": db,
        "route": "direct"
    }
    
    # LangSmith tracing will automatically trace this .ainvoke call if LANGCHAIN_TRACING_V2 is set
    try:
        final_state = await compiled_graph.ainvoke(inputs)
        return final_state["messages"][-1].content
    except Exception as e:
        print("LangGraph Error:", e)
        # Fallback for Cerebras 402/rate limits just like before
        content_text = user_message.lower()
        if any(w in content_text for w in ["book", "borrow", "author", "title", "read", "harry potter", "search"]):
            from app.services.tool_dispatcher import execute_tool
            res = execute_tool("search_books", {"query": user_message}, user_id, db)
            if not res or not res.get("results"):
                return "I searched the library catalog, but unfortunately I didn't find any matching books."
            titles = [b["title"] for b in res["results"]]
            return f"I found some books that match your query: {', '.join(titles)}."
        else:
            from app.services.qdrant_service import search_library
            res = await search_library(user_message)
            if res:
                return f"According to library policy: {res[0]}"
            return "I couldn't find any library policies related to that."
