"""
Seed the Qdrant vector database with library knowledge.

This script creates rich text descriptions for every book in the catalog
and uploads them as searchable vector points into Qdrant.

Usage (run from the project root):
    python -m app.scripts.seed_qdrant

How it works:
    1. Each book is converted to a plain-English description string
    2. That string is embedded via Gemini text-embedding-004 (768 dims)
    3. The vector + payload (title, author, genre, content) are stored in Qdrant
    4. At chat time, user queries are embedded and Qdrant returns the closest matches
       which are injected into the Gemini system prompt as grounded context

Run this again whenever you add new books or update descriptions.
Teacher's data can be added to LIBRARY_DOCS below and re-run.
"""

import asyncio
import sys
import os

# Ensure project root is on the path when running as a script
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from app.services.qdrant_service import upsert_documents, ensure_collection_exists, get_qdrant_client

# ── Library knowledge to store in Qdrant ─────────────────────────────────────
# Each entry becomes one searchable point.
# 'text' is what gets embedded — make it descriptive so semantic search works well.
# 'content' is what gets returned to Gemini as context.
# Add your teacher's data here later and re-run the script.

LIBRARY_DOCS = [
    {
        "text": "The Hobbit fantasy adventure J.R.R. Tolkien hobbits wizards dragons Middle Earth",
        "content": "Title: The Hobbit | Author: J.R.R. Tolkien | Genre: Fantasy | A classic fantasy adventure following Bilbo Baggins on a quest with dwarves and a wizard to reclaim a treasure guarded by the dragon Smaug.",
    },
    {
        "text": "Mistborn fantasy magic system allomancy Brandon Sanderson epic trilogy",
        "content": "Title: Mistborn | Author: Brandon Sanderson | Genre: Fantasy | An epic fantasy set in a world of ash and mist where certain individuals can ingest metals to gain magical powers. A heist story meets epic worldbuilding. Currently unavailable.",
    },
    {
        "text": "Dune science fiction desert planet spice Frank Herbert epic space opera",
        "content": "Title: Dune | Author: Frank Herbert | Genre: Sci-Fi | A landmark science fiction novel set on the desert planet Arrakis, following Paul Atreides as he navigates politics, religion, and survival in a world controlled by a precious spice.",
    },
    {
        "text": "1984 George Orwell dystopian totalitarian surveillance society Big Brother",
        "content": "Title: 1984 | Author: George Orwell | Genre: Dystopian | A haunting vision of a totalitarian future where the government controls all thought and history. One of the most influential political novels ever written.",
    },
    {
        "text": "Pride and Prejudice Jane Austen romance Victorian England love marriage social class",
        "content": "Title: Pride and Prejudice | Author: Jane Austen | Genre: Romance | A witty and sharp novel of manners following Elizabeth Bennet and the proud Mr. Darcy. A timeless romance about love, class, and personal growth.",
    },
    {
        "text": "The Great Gatsby F. Scott Fitzgerald American dream Jazz Age wealth parties",
        "content": "Title: The Great Gatsby | Author: F. Scott Fitzgerald | Genre: Classic | A lyrical portrait of the Roaring Twenties and the American Dream, told through the tragic obsession of the mysterious millionaire Jay Gatsby.",
    },
    {
        "text": "Atomic Habits James Clear self-help habits productivity routine improvement small changes",
        "content": "Title: Atomic Habits | Author: James Clear | Genre: Self-Help | A practical guide to building good habits and breaking bad ones. Uses science and real-world examples to show how tiny changes lead to remarkable results.",
    },
    {
        "text": "Sapiens Yuval Noah Harari human history evolution civilization culture non-fiction",
        "content": "Title: Sapiens | Author: Yuval Noah Harari | Genre: Non-Fiction | A sweeping narrative of human history from the Stone Age to the present day, exploring how Homo sapiens came to dominate the planet.",
    },
    {
        "text": "The Da Vinci Code Dan Brown thriller mystery art history secret society",
        "content": "Title: The Da Vinci Code | Author: Dan Brown | Genre: Thriller | A fast-paced thriller in which a Harvard symbologist uncovers a series of clues hidden in Leonardo da Vinci's works that lead to a dangerous secret.",
    },
    {
        "text": "Harry Potter Sorcerer Stone J.K. Rowling magic wizard school Hogwarts children fantasy",
        "content": "Title: Harry Potter and the Sorcerer's Stone | Author: J.K. Rowling | Genre: Fantasy | The first book in the beloved Harry Potter series. A young boy discovers he is a wizard and begins his education at Hogwarts School of Witchcraft and Wizardry.",
    },
    {
        "text": "The Alchemist Paulo Coelho spiritual journey destiny dreams travel fable",
        "content": "Title: The Alchemist | Author: Paulo Coelho | Genre: Fiction | An inspirational fable about a young Andalusian shepherd who travels to Egypt in search of treasure, learning along the way about the importance of following your dreams.",
    },
    {
        "text": "To Kill a Mockingbird Harper Lee racial injustice American South classic moral courage",
        "content": "Title: To Kill a Mockingbird | Author: Harper Lee | Genre: Classic | A Pulitzer Prize-winning novel set in 1930s Alabama, exploring racial injustice and moral growth through the eyes of young Scout Finch and her lawyer father Atticus. Currently unavailable.",
    },
    {
        "text": "Gone Girl Gillian Flynn psychological thriller mystery marriage suspense",
        "content": "Title: Gone Girl | Author: Gillian Flynn | Genre: Thriller | A gripping psychological thriller about the disappearance of Amy Dunne on her fifth wedding anniversary, and the dark secrets that unravel in the investigation.",
    },
    {
        "text": "The Martian Andy Weir science fiction survival stranded astronaut Mars",
        "content": "Title: The Martian | Author: Andy Weir | Genre: Sci-Fi | A gripping survival story about an astronaut stranded alone on Mars who must use science, ingenuity, and dark humor to stay alive until rescue is possible.",
    },
    # ── Library general FAQs (also stored as searchable knowledge) ───────────
    {
        "text": "library hours opening times schedule when is library open",
        "content": "Library Hours: The library is open Monday to Friday 9am–8pm, Saturday 10am–6pm, and closed on Sunday.",
    },
    {
        "text": "borrow loan book rules how many books can I borrow limit",
        "content": "Borrowing Policy: Members can borrow up to 3 books at a time. Loan period is 14 days. Books can be renewed once if no one else has requested them.",
    },
    {
        "text": "return overdue late fee fine penalty",
        "content": "Return Policy: Books must be returned within 14 days. Late returns incur a small fine. Return books at the front desk or the drop box near the entrance.",
    },
    {
        "text": "membership how to join library card register sign up",
        "content": "Membership: Anyone can join the library for free. Visit the front desk with a valid ID to get your library card. Students get automatic membership through the institution.",
    },
]


async def main() -> None:
    client = get_qdrant_client()
    if client is None:
        print(
            "ERROR: Qdrant credentials not set.\n"
            "Please add QDRANT_URL and QDRANT_API_KEY to your .env file."
        )
        return

    print(f"Connecting to Qdrant at {__import__('app.core.config', fromlist=['settings']).settings.QDRANT_URL}")
    ensure_collection_exists(client)

    print(f"Uploading {len(LIBRARY_DOCS)} documents...")
    await upsert_documents(LIBRARY_DOCS)
    print("Done! Your library knowledge is now searchable in Qdrant.")
    print("You can add your teacher's data to LIBRARY_DOCS in this file and re-run.")


if __name__ == "__main__":
    asyncio.run(main())
