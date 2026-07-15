from app.core.database import SessionLocal
from app.services.library_tools import (
    search_books, check_availability, borrow_book, return_book, get_my_borrowed_books
)
from app.schemas.tool_schemas import (
    SearchBooksArgs, CheckAvailabilityArgs, BorrowBookArgs, ReturnBookArgs, GetMyBorrowedBooksArgs
)

TEST_USER_ID = 1  # change to a real user id from your users table

db = SessionLocal()

print("\n--- search_books('fantasy') ---")
print(search_books(SearchBooksArgs(query="fantasy"), db))

print("\n--- check_availability(book_id=2) — Mistborn, should be 0 ---")
print(check_availability(CheckAvailabilityArgs(book_id=2), db))

print("\n--- borrow_book(book_id=1) — The Hobbit, should succeed ---")
print(borrow_book(BorrowBookArgs(user_id=TEST_USER_ID, book_id=1), db))

print("\n--- borrow_book(book_id=2) — Mistborn, should FAIL (0 copies) ---")
print(borrow_book(BorrowBookArgs(user_id=TEST_USER_ID, book_id=2), db))

print("\n--- get_my_borrowed_books ---")
print(get_my_borrowed_books(GetMyBorrowedBooksArgs(user_id=TEST_USER_ID), db))

print("\n--- return_book(book_id=1) ---")
print(return_book(ReturnBookArgs(user_id=TEST_USER_ID, book_id=1), db))

db.close()