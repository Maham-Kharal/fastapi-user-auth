from pydantic import BaseModel


class SearchBooksArgs(BaseModel):
    query: str


class CheckAvailabilityArgs(BaseModel):
    book_id: int


class BorrowBookArgs(BaseModel):
    user_id: int
    book_id: int


class ReturnBookArgs(BaseModel):
    user_id: int
    book_id: int


class GetMyBorrowedBooksArgs(BaseModel):
    user_id: int