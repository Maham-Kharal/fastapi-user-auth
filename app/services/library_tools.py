from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.models import Book, Loan
from app.schemas.tool_schemas import (
    SearchBooksArgs,
    CheckAvailabilityArgs,
    BorrowBookArgs,
    ReturnBookArgs,
    GetMyBorrowedBooksArgs,
)

MAX_BOOKS_PER_USER = 3
LOAN_PERIOD_DAYS = 14


STOP_WORDS = {
    "can", "i", "borrow", "a", "book", "books", "the", "tell", "me", "what", "are",
    "is", "available", "availableat", "moment", "now", "please", "show", "list",
    "get", "find", "search", "check", "for", "in", "of", "to", "okay", "so"
}


def search_books(args: SearchBooksArgs, db: Session) -> list[dict]:
    raw_query = (args.query or "").strip().lower()

    # 1. Exact or partial substring match
    if raw_query:
        results = (
            db.query(Book)
            .filter(
                (Book.title.ilike(f"%{raw_query}%"))
                | (Book.author.ilike(f"%{raw_query}%"))
                | (Book.genre.ilike(f"%{raw_query}%"))
            )
            .all()
        )
        if results:
            return [
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "available_copies": b.available_copies,
                    "total_copies": b.total_copies,
                }
                for b in results
            ]

    # 2. Extract meaningful keywords after stripping stop words
    words = [
        w
        for w in raw_query.replace(".", "").replace(",", "").replace("?", "").split()
        if w not in STOP_WORDS and len(w) > 1
    ]

    if words:
        for word in words:
            results = (
                db.query(Book)
                .filter(
                    (Book.title.ilike(f"%{word}%"))
                    | (Book.author.ilike(f"%{word}%"))
                    | (Book.genre.ilike(f"%{word}%"))
                )
                .all()
            )
            if results:
                return [
                    {
                        "id": b.id,
                        "title": b.title,
                        "author": b.author,
                        "available_copies": b.available_copies,
                        "total_copies": b.total_copies,
                    }
                    for b in results
                ]

    # 3. Fallback: Return all books in the catalog
    all_books = db.query(Book).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "available_copies": b.available_copies,
            "total_copies": b.total_copies,
        }
        for b in all_books
    ]

def check_availability(args: CheckAvailabilityArgs, db: Session) -> dict:
    book = db.query(Book).filter(Book.id == args.book_id).first()
    if not book:
        return {"error": "Book not found"}
    return {
        "title": book.title,
        "available_copies": book.available_copies,
        "total_copies": book.total_copies,
    }


def borrow_book(args: BorrowBookArgs, db: Session) -> dict:
    book = db.query(Book).filter(Book.id == args.book_id).first()
    if not book:
        return {"success": False, "reason": "Book not found"}

    # --- guardrail 1: the 3-book limit, enforced in code, not just the prompt ---
    active_loans = (
        db.query(Loan)
        .filter(Loan.user_id == args.user_id, Loan.status == "borrowed")
        .count()
    )
    if active_loans >= MAX_BOOKS_PER_USER:
        return {"success": False, "reason": f"You already have {MAX_BOOKS_PER_USER} books borrowed. Return one before borrowing another."}

    # --- guardrail 2: real copy availability, also enforced in code ---
    if book.available_copies <= 0:
        return {"success": False, "reason": f"'{book.title}' has no available copies right now."}

    # both checks passed — perform the borrow
    due_date = datetime.utcnow() + timedelta(days=LOAN_PERIOD_DAYS)
    loan = Loan(book_id=book.id, user_id=args.user_id, due_date=due_date, status="borrowed")
    book.available_copies -= 1

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return {
        "success": True,
        "book_title": book.title,
        "due_date": due_date.strftime("%Y-%m-%d"),
        "loan_id": loan.id,
    }


def return_book(args: ReturnBookArgs, db: Session) -> dict:
    loan = (
        db.query(Loan)
        .filter(Loan.user_id == args.user_id, Loan.book_id == args.book_id, Loan.status == "borrowed")
        .first()
    )
    if not loan:
        return {"success": False, "reason": "No active loan found for this book under your account."}

    book = db.query(Book).filter(Book.id == args.book_id).first()

    loan.returned_at = datetime.utcnow()
    loan.status = "returned"
    if book:
        book.available_copies += 1

    db.commit()

    return {"success": True, "book_title": book.title if book else "Unknown"}


def get_my_borrowed_books(args: GetMyBorrowedBooksArgs, db: Session) -> list[dict]:
    loans = (
        db.query(Loan)
        .filter(Loan.user_id == args.user_id, Loan.status == "borrowed")
        .all()
    )
    result = []
    for loan in loans:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        result.append({
            "book_title": book.title if book else "Unknown",
            "due_date": loan.due_date.strftime("%Y-%m-%d"),
            "borrowed_at": loan.borrowed_at.strftime("%Y-%m-%d"),
        })
    return result