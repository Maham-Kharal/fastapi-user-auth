from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from pydantic import Field

@tool
def search_books(query: str = Field(description="Title, author, or genre to search for")) -> dict:
    """Search the library catalog for books."""
    pass

@tool
def check_availability(book_id: int = Field(description="ID of the book")) -> dict:
    """Check if a specific book is currently available to borrow."""
    pass

@tool
def borrow_book(book_id: int = Field(description="ID of the book to borrow")) -> dict:
    """Borrow a book from the library."""
    pass

@tool
def return_book(book_id: int = Field(description="ID of the book to return")) -> dict:
    """Return a borrowed book to the library."""
    pass

@tool
def get_my_borrowed_books() -> dict:
    """Get a list of all books currently borrowed by the user."""
    pass

@tool
def search_knowledge_base(query: str = Field(description="The policy question or topic to search for")) -> dict:
    """Search the library's policy knowledge base (hours, borrowing rules, fines, membership, etc.)."""
    pass

CATALOG_TOOLS = [search_books, check_availability, borrow_book, return_book, get_my_borrowed_books]
POLICY_TOOLS = [search_knowledge_base]
