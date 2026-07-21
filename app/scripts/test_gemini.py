import asyncio
from app.core.database import SessionLocal
from app.services.gemini_client import ask_gemini_with_tools

async def main():
    db = SessionLocal()
    history = [{"role": "user", "content": "do you have any fantasy book"}]
    print("Testing ask_gemini_with_tools with query: 'do you have any fantasy book'")
    try:
        res = await ask_gemini_with_tools(history, 1, db)
        print("Response:\n", res)
    except Exception as e:
        print("Error encountered:", e)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
