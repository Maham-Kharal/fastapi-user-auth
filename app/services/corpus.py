# Raw library documents used for chunking, indexing, and evaluation.
RAW_DOCUMENTS = [
    {
        "id": 1,
        "title": "Library Hours & General Schedule Policy",
        "text": (
            "The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM "
            "in the morning and close at 8:00 PM in the evening to accommodate students and local residents. On "
            "Saturdays, we operate on reduced hours, opening at 10:00 AM and closing at 6:00 PM. The library is closed "
            "on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until "
            "midnight. Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. "
            "On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announcements."
        ),
    },
    {
        "id": 2,
        "title": "Borrowing Limit & Loan Extension Policy",
        "text": (
            "Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical "
            "books at any given time. The default loan period is 14 calendar days (two weeks) from the checkout date. "
            "If you need more time, a book can be renewed exactly once for an additional 14 days, provided that no "
            "other library patron has placed a hold or reservation on that book. Renewals can be requested online, "
            "via our mobile app, or at the front desk. Reference books, current issues of periodicals, and rare "
            "manuscripts cannot be checked out and must be read within the library reading room."
        ),
    },
    {
        "id": 3,
        "title": "Overdue Book Fines & Return Protocol",
        "text": (
            "All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return "
            "points include the main reception desk inside the library or the external drop box located next to the "
            "front entrance, which is available 24/7. If a book is returned late, an overdue fine of $0.50 per day "
            "per book is automatically charged to the member's account. There is a grace period of 2 days, meaning "
            "no fine is charged if the book is returned within 16 days. If a book is lost or damaged beyond repair, "
            "the member must pay the replacement cost of the book plus a processing fee of $10.00."
        ),
    },
    {
        "id": 4,
        "title": "Membership Registration & Digital Access Policy",
        "text": (
            "Library membership is free of charge for all local residents and students. To register, visit the front "
            "desk and present a valid government-issued photo ID along with proof of address (such as a utility bill "
            "or student card). Students enrolled in the local university receive automatic membership using their "
            "student ID card. Once registered, members receive a physical library card and a PIN code for digital access. "
            "The digital library provides access to over 10,000 e-books and academic journals. Do not share your "
            "library card or PIN; members are responsible for all items checked out under their name."
        ),
    },
    {
        "id": 5,
        "title": "Fantasy Literature Profile: J.R.R. Tolkien's The Hobbit",
        "text": (
            "The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. "
            "It introduces the reader to the magical world of Middle-earth. The story follows the quest of Bilbo Baggins, "
            "a home-loving hobbit, who is hired by the wizard Gandalf and a company of thirteen dwarves led by Thorin "
            "Oakenshield. Their dangerous mission is to reclaim the Lonely Mountain and its vast treasure from Smaug, "
            "a fearsome and greedy dragon. Along the way, Bilbo finds a mysterious magic ring that makes him invisible, "
            "which plays a major role in Tolkien's sequel, The Lord of the Rings."
        ),
    },
    {
        "id": 6,
        "title": "Sci-Fi Literature Profile: Frank Herbert's Dune",
        "text": (
            "Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant "
            "future in an interstellar empire, it tells the story of young Paul Atreides as his family accepts control of "
            "the desert planet Arrakis. Arrakis is the only source of the 'spice' melange, the most valuable substance in "
            "the universe, which enables space travel and extends human life. The novel explores themes of politics, "
            "religion, ecology, and human power. Paul must navigate betrayal, lead the indigenous Fremen people, and "
            "fulfill a prophecy that will change the galaxy forever."
        ),
    },
]

# Core evaluation questions mapped to expected document IDs.
EVAL_QUESTIONS = [
    {
        "query": "What time does the library close on Saturdays?",
        "expected_doc_id": 1,
    },
    {
        "query": "How many books can a member check out at once?",
        "expected_doc_id": 2,
    },
    {
        "query": "What is the penalty if I return a library book late?",
        "expected_doc_id": 3,
    },
    {
        "query": "What documents do I need to bring to sign up for a library card?",
        "expected_doc_id": 4,
    },
    {
        "query": "Who are the main characters in the fantasy book The Hobbit?",
        "expected_doc_id": 5,
    },
    {
        "query": "Why is the planet Arrakis important in Frank Herbert's Dune?",
        "expected_doc_id": 6,
    },
]
