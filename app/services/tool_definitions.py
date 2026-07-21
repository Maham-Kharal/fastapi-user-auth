LIBRARY_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "search_books",
                "description": "Search the library catalog by title, author, or genre keyword",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search term — a title, author name, or genre"}
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "check_availability",
                "description": "Check how many copies of a specific book are currently available",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "The ID of the book to check"}
                    },
                    "required": ["book_id"],
                },
            },
            {
                "name": "borrow_book",
                "description": "Borrow a book for the current user, if copies are available and they haven't hit the 3-book limit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "The ID of the book to borrow"}
                    },
                    "required": ["book_id"],
                },
            },
            {
                "name": "return_book",
                "description": "Return a book the current user previously borrowed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "The ID of the book to return"}
                    },
                    "required": ["book_id"],
                },
            },
            {
                "name": "get_my_borrowed_books",
                "description": "Get the list of books the current user currently has borrowed",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        ]
    }
]