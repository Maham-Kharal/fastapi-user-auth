from sqlalchemy.orm import Session

from app.services.library_tools import (
    search_books, check_availability, borrow_book, return_book, get_my_borrowed_books
)
from app.schemas.tool_schemas import (
    SearchBooksArgs, CheckAvailabilityArgs, BorrowBookArgs, ReturnBookArgs, GetMyBorrowedBooksArgs
)


def execute_tool(name: str, args: dict, user_id: int, db: Session) -> dict:
    if name == "search_books":
        return {"results": search_books(SearchBooksArgs(**args), db)}

    elif name == "check_availability":
        return check_availability(CheckAvailabilityArgs(**args), db)

    elif name == "borrow_book":
        return borrow_book(BorrowBookArgs(user_id=user_id, book_id=args["book_id"]), db)

    elif name == "return_book":
        return return_book(ReturnBookArgs(user_id=user_id, book_id=args["book_id"]), db)

    elif name == "get_my_borrowed_books":
        return {"results": get_my_borrowed_books(GetMyBorrowedBooksArgs(user_id=user_id), db)}

    else:
        return {"error": f"Unknown tool: {name}"}