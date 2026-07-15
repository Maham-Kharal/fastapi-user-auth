from app.core.database import SessionLocal
from app.models.models import Book

books_data = [
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy", "total_copies": 3, "available_copies": 3},
    {"title": "Mistborn", "author": "Brandon Sanderson", "genre": "fantasy", "total_copies": 2, "available_copies": 0},
    {"title": "Dune", "author": "Frank Herbert", "genre": "sci-fi", "total_copies": 4, "available_copies": 2},
    {"title": "1984", "author": "George Orwell", "genre": "dystopian", "total_copies": 3, "available_copies": 3},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "romance", "total_copies": 2, "available_copies": 1},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "classic", "total_copies": 3, "available_copies": 3},
    {"title": "Atomic Habits", "author": "James Clear", "genre": "self-help", "total_copies": 5, "available_copies": 4},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "genre": "non-fiction", "total_copies": 2, "available_copies": 2},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "genre": "thriller", "total_copies": 3, "available_copies": 1},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "fantasy", "total_copies": 4, "available_copies": 3},
    {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "fiction", "total_copies": 2, "available_copies": 2},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "classic", "total_copies": 2, "available_copies": 0},
    {"title": "Gone Girl", "author": "Gillian Flynn", "genre": "thriller", "total_copies": 2, "available_copies": 2},
    {"title": "The Martian", "author": "Andy Weir", "genre": "sci-fi", "total_copies": 3, "available_copies": 3},
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Book).count()
        if existing > 0:
            print(f"Books table already has {existing} rows — skipping seed.")
            return
        for b in books_data:
            db.add(Book(**b))
        db.commit()
        print(f"Seeded {len(books_data)} books.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()