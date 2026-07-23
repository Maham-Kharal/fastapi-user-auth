import asyncio
from app.core.database import SessionLocal
from app.services.langgraph_workflow import run_langgraph_orchestrator as run_orchestrator

async def run_query(query: str, db):
    print(f"\n--- Testing Query: '{query}' ---")
    try:
        reply = await run_orchestrator(query, 1, db)
        print("Reply:\n", reply)
    except Exception as e:
        print("Error encountered:", e)

async def main():
    db = SessionLocal()
    try:
        # 1. Catalog-only query
        await run_query("do you have any fantasy book", db)
        
        # 2. Policy-only query
        await run_query("what are the library hours on Saturday?", db)
        
        # 3. Mixed query
        await run_query("is Dune available, and what is the overdue book fine?", db)
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
