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
    {
        "id": 7,
        "title": "History of the Library Foundation",
        "text": (
            "The library was founded in 1924 by a group of local citizens who wanted to promote literacy. "
            "It began as a single room with 500 books and has grown to its current size over a century. "
            "The historical archives contain original letters, photographs, and records from the early years."
        ),
    },
    {
        "id": 8,
        "title": "Children's Storytime & Reading Area Rules",
        "text": (
            "The children's section is designed for kids under 12 years old. Storytime sessions are held "
            "every Tuesday and Thursday morning starting at 10:30 AM. Parents or guardians must accompany "
            "children at all times. Please ensure toys and books are returned to their shelves after use."
        ),
    },
    {
        "id": 9,
        "title": "Quiet Study Rooms Booking Policy",
        "text": (
            "Quiet study rooms are available for individual or group study. Rooms can be booked for up "
            "to 2 hours per day. Bookings must be made in advance online or at the information desk. "
            "If a room is not occupied within 15 minutes of the start time, the booking is cancelled."
        ),
    },
    {
        "id": 10,
        "title": "Interlibrary Loan Service",
        "text": (
            "If our library does not have a book you need, you can request it through interlibrary loan. "
            "We partner with other libraries across the region to share resources. It typically takes "
            "5 to 7 business days for a book to arrive. Loan periods are set by the lending library."
        ),
    },
    {
        "id": 11,
        "title": "Donations & Gift Books Guidelines",
        "text": (
            "We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the "
            "designated bin near the side entrance. We accept fiction, non-fiction, and children's books. "
            "Items that we cannot add to our collection are sold in the annual library book sale."
        ),
    },
    {
        "id": 12,
        "title": "Volunteer Program & Community Service",
        "text": (
            "The library offers volunteer opportunities for teens and adults. Volunteers help with shelving "
            "books, organizing events, and assisting patrons. High school students can earn community service "
            "hours. Interested individuals must fill out an application and pass a background check."
        ),
    },
    {
        "id": 13,
        "title": "Lost and Found Items Policy",
        "text": (
            "Items found in the library are turned in to the front desk. Valuable items such as phones, "
            "wallets, and keys are kept in a secure locker. Unclaimed items are held for 30 days. "
            "After 30 days, unclaimed items are donated to local charities or disposed of."
        ),
    },
    {
        "id": 14,
        "title": "Computer Lab and Internet Code of Conduct",
        "text": (
            "Our computer lab offers free internet access and printing services. Patrons must log in using "
            "their library card number. Printing costs $0.10 per page for black and white, and $0.50 for color. "
            "Viewing inappropriate content or engaging in illegal activities is strictly prohibited."
        ),
    },
    {
        "id": 15,
        "title": "Noise Level & Behavior in Silent Zones",
        "text": (
            "To provide a productive environment, the third floor is designated as a silent study zone. "
            "No talking or group discussions are allowed on this floor. Phone calls must be taken in the "
            "lobby. Headphones must be used for audio devices and kept at a low volume."
        ),
    },
    {
        "id": 16,
        "title": "Food and Beverage Regulations",
        "text": (
            "Patrons may bring covered drinks and small snacks into the library. Hot food, meals, and "
            "messy snacks are not allowed in the study areas. Please dispose of trash in the recycling "
            "and waste bins provided throughout the building. Report any spills to staff immediately."
        ),
    },
    {
        "id": 17,
        "title": "Classic Literature Profile: Herman Melville's Moby Dick",
        "text": (
            "Moby-Dick is an epic novel written by Herman Melville and published in 1851. It details the "
            "voyage of the whaling ship Pequod, commanded by Captain Ahab. Ahab is obsessed with seeking "
            "revenge on Moby Dick, a giant white sperm whale that previously bit off his leg."
        ),
    },
    {
        "id": 18,
        "title": "Classic Literature Profile: Jane Austen's Pride and Prejudice",
        "text": (
            "Pride and Prejudice is a classic romantic novel of manners written by Jane Austen in 1813. "
            "It follows the character development of Elizabeth Bennet, who learns about the error of "
            "making hasty judgments and comes to appreciate the difference between superficial and real goodness."
        ),
    },
    {
        "id": 19,
        "title": "Mystery Literature Profile: Arthur Conan Doyle's Sherlock Holmes",
        "text": (
            "The Adventures of Sherlock Holmes is a collection of detective stories by Arthur Conan Doyle. "
            "It features the brilliant consulting detective Sherlock Holmes and his companion Dr. John Watson. "
            "Together they solve complex cases in Victorian London using Holmes's signature deductive reasoning."
        ),
    },
    {
        "id": 20,
        "title": "Scientific Literature Profile: Stephen Hawking's A Brief History of Time",
        "text": (
            "A Brief History of Time is a popular-science book written by English physicist Stephen Hawking. "
            "First published in 1988, it explains complex topics in cosmology like the Big Bang, black holes, "
            "and light cones, to non-specialist readers using simple language and illustrations."
        ),
    },
    {
        "id": 21,
        "title": "Library Parking and Transportation Policy",
        "text": (
            "Free parking is available for all library visitors in the north parking lot. Patrons must display "
            "a valid parking permit on their dashboard if parking for more than three hours. Bicycle racks "
            "are located near the main entrance. Public buses stop directly in front of the library every 20 minutes."
        ),
    },
    {
        "id": 22,
        "title": "Meeting and Event Space Reservations",
        "text": (
            "The library has a community room available for public meetings, workshops, and events. The room "
            "can accommodate up to 50 people and features a projector and sound system. Reservations must "
            "be made by a registered library member at least two weeks in advance. A fee of $25 per hour applies."
        ),
    },
    {
        "id": 23,
        "title": "Exhibits, Displays, and Bulletin Board Policy",
        "text": (
            "The library maintains bulletin boards and display cases to highlight local events, art, and "
            "culture. Submissions for the bulletin board must be approved by the library director. Items "
            "must be non-commercial, non-sectarian, and of general community interest. Postings are limited to 30 days."
        ),
    },
    {
        "id": 24,
        "title": "Emergency Evacuation and Safety Protocol",
        "text": (
            "In the event of an emergency, such as a fire or severe weather, all patrons must follow the "
            "instructions of library staff. Emergency exits are clearly marked on all floors. Evacuation routes "
            "lead to the south parking lot. Please do not use the elevators during an evacuation."
        ),
    },
    {
        "id": 25,
        "title": "Privacy and Patron Records Policy",
        "text": (
            "We are committed to protecting your privacy. The library does not disclose information about "
            "borrowed books, search histories, or personal details to third parties unless required by law. "
            "Patron records are kept strictly confidential and are only accessed by authorized staff members."
        ),
    },
    {
        "id": 26,
        "title": "Acceptable Use of Library Materials",
        "text": (
            "Patrons are expected to treat all library materials with care. Highlighting, writing, or "
            "folding pages in library books is considered damage. Materials must be returned in the same "
            "condition they were borrowed. Repeat offenders may have their borrowing privileges suspended."
        ),
    }
]

# Core evaluation questions mapped to expected document IDs.
EVAL_QUESTIONS = [
    {"query": "Is the library open on New Year's Day?", 
     "expected_doc_id": 1},
    {"query": "Are the library hours different during finals?", 
     "expected_doc_id": 1},
    {"query": "What time can I visit on a weekday morning?", 
     "expected_doc_id": 1},
    {"query": "Can I renew a book more than one time?", 
     "expected_doc_id": 2},
    {"query": "Can I take a magazine or reference book home with me?", 
     "expected_doc_id": 2},
    {"query": "How much extra time do I get after the due date before I'm charged?", 
     "expected_doc_id": 3},
    {"query": "What happens if I destroy a book I borrowed?", 
     "expected_doc_id": 3},
    {"query": "Where can I drop off books after closing time?", 
     "expected_doc_id": 3},
    {"query": "Can someone without a fixed home address still sign up?", 
     "expected_doc_id": 4},
    {"query": "Do university students need to fill out a separate application?", 
     "expected_doc_id": 4},
    {"query": "How many electronic books can I access with my membership?", 
     "expected_doc_id": 4},
    {"query": "What object does Bilbo find on his journey that becomes important later?", 
     "expected_doc_id": 5},
    {"query": "Which mountain do the dwarves want to reclaim from the dragon?", 
     "expected_doc_id": 5},
    {"query": "What natural resource makes space travel possible in Dune, and where is it found?", 
     "expected_doc_id": 6},
]