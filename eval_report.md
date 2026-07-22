# RAG Evaluation Comparison Report

This report compares the impact of 5 retrieval configurations on the retrieval of relevant chunks and final answers.

## Configuration Summary & Hit Rates

| Config | Strategy | Chunk Size | Overlap | Top K | Hybrid | Reranker | Hit Rate | Precision | Recall | F1 Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Config 1: Fixed-Size Small (Dense)** | fixed | 250 | 50 | 3 | False | False | **100.0%** | 0.33 | 1.00 | 0.50 |
| **Config 2: Fixed-Size Large (Dense)** | fixed | 1000 | 200 | 3 | False | False | **100.0%** | 0.33 | 1.00 | 0.50 |
| **Config 3: Semantic (Dense)** | semantic | auto | auto | 3 | False | False | **85.2%** | 0.28 | 0.85 | 0.43 |
| **Config 4: Semantic (Hybrid RRF)** | semantic | auto | auto | 3 | True | False | **96.3%** | 0.32 | 0.96 | 0.48 |
| **Config 5: Semantic (Hybrid + Reranker)** | semantic | auto | auto | 3 | True | True | **96.3%** | 0.32 | 0.96 | 0.48 |

---

## Detailed Query Logs

Below is the breakdown of exactly which chunks were retrieved, in what order, and what answer was produced for each query under each configuration.

### Config 1: Fixed-Size Small (Dense)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** 
In addition to standard weekly hours, all branches close early at 2:00 PM on the day before Thanksgiving and
Christmas Eve. Members should check the library website or call ahead during the last week...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 
In addition to standard weekly hours, all branches close early at 2:00 PM on the day before Thanksgiving and
Christmas Eve. Members should check the ...
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 1] until midnight. Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually c...

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** n Saturdays, we operate on reduced hours, opening at 10:00 AM and closing at 6:00 PM. The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] n Saturdays, we operate on reduced hours, opening at 10:00 AM and closing at 6:00 PM. The library is closed on Sundays to allow for deep cleaning and ...
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 28] 
In addition to standard weekly hours, all branches close early at 2:00 PM on the day before Thanksgiving and
Christmas Eve. Members should check the ...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** until midnight. Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] until midnight. Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually c...
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 9] ied within 15 minutes of the start time, the booking is cancelled....

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** out date. If you need more time, a book can be renewed exactly once for an additional 14 days, provided that no other library patron has placed a hold or reservation on that book. Renewals can be requ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] out date. If you need more time, a book can be renewed exactly once for an additional 14 days, provided that no other library patron has placed a hold...
  2. [Doc ID: 29] renewals
DVDs & Blu-rays
7 days
1 renewal
Audiobooks (physical)
14 days
2 renewals
Magazines & periodicals
14 days
1 renewal
Video games
7 days
1 rene...
  3. [Doc ID: 29]  items checked out on a lost card before it is
reported.
3. Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & ...

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** ested online, via our mobile app, or at the front desk. Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] ested online, via our mobile app, or at the front desk. Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 29]  Reservations
Members may place holds on items that are currently checked out or located at another branch. A member may
have up to 15 active holds at...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** d Items
If an item is not returned within 30 days of its due date, it is considered lost and the member's account is
charged the item's full replacement cost plus a $5.00 processing fee. If the item i...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] d Items
If an item is not returned within 30 days of its due date, it is considered lost and the member's account is
charged the item's full replaceme...
  2. [Doc ID: 3] s, meaning no fine is charged if the book is returned within 16 days. If a book is lost or damaged beyond repair, the member must pay the replacement ...
  3. [Doc ID: 3] to the front entrance, which is available 24/7. If a book is returned late, an overdue fine of $0.50 per day per book is automatically charged to the ...

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Materials must be returned in the same condition they were...
- **Retrieved Chunks Order:**
  1. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Material...
  2. [Doc ID: 26]  borrowed. Repeat offenders may have their borrowing privileges suspended....
  3. [Doc ID: 3] s, meaning no fine is charged if the book is returned within 16 days. If a book is lost or damaged beyond repair, the member must pay the replacement ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside the library or the external drop box located next ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...
  2. [Doc ID: 3] to the front entrance, which is available 24/7. If a book is returned late, an overdue fine of $0.50 per day per book is automatically charged to the ...
  3. [Doc ID: 32] rior book drop, which is checked daily including weekends.
What happens if I move out of the county?
Your card remains valid until its three-year expi...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** nterested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] nterested individuals must fill out an application and pass a background check....
  2. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** nterested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] nterested individuals must fill out an application and pass a background check....
  2. [Doc ID: 25] ds are kept strictly confidential and are only accessed by authorized staff members....
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** r digital access. The digital library provides access to over 10,000 e-books and academic journals. Do not share your library card or PIN; members are responsible for all items checked out under their...
- **Retrieved Chunks Order:**
  1. [Doc ID: 4] r digital access. The digital library provides access to over 10,000 e-books and academic journals. Do not share your library card or PIN; members are...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 30] igital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their ...

**Question 12:** What object does Bilbo find on his journey that becomes important later?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** vast treasure from Smaug, a fearsome and greedy dragon. Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] vast treasure from Smaug, a fearsome and greedy dragon. Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a maj...
  2. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  3. [Doc ID: 5]  Bilbo Baggins, a home-loving hobbit, who is hired by the wizard Gandalf and a company of thirteen dwarves led by Thorin Oakenshield. Their dangerous ...

**Question 13:** Which mountain do the dwarves want to reclaim from the dragon?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:**  Bilbo Baggins, a home-loving hobbit, who is hired by the wizard Gandalf and a company of thirteen dwarves led by Thorin Oakenshield. Their dangerous mission is to reclaim the Lonely Mountain and its ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5]  Bilbo Baggins, a home-loving hobbit, who is hired by the wizard Gandalf and a company of thirteen dwarves led by Thorin Oakenshield. Their dangerous ...
  2. [Doc ID: 5] vast treasure from Smaug, a fearsome and greedy dragon. Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a maj...
  3. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** accepts control of the desert planet Arrakis. Arrakis is the only source of the 'spice' melange, the most valuable substance in the universe, which enables space travel and extends human life. The nov...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] accepts control of the desert planet Arrakis. Arrakis is the only source of the 'spice' melange, the most valuable substance in the universe, which en...
  2. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  3. [Doc ID: 6] el explores themes of politics, religion, ecology, and human power. Paul must navigate betrayal, lead the indigenous Fremen people, and fulfill a prop...

**Question 15:** What does the document state regarding: Riverbend Public Library Member Handbook & Policy Guide Effective 2026 Edition 123 Elm Str?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  2. [Doc ID: 28]  of December, as
reduced hours may apply between Christmas and New Year's Day.
2. Membership & Library Cards
Anyone who lives, works, attends school, ...
  3. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...

**Question 16:** What does the document state regarding: Hours & Locations Riverbend Public Library operates three branches across the city, each w?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed on major public holidays, including New Year's D...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...
  2. [Doc ID: 28]  of December, as
reduced hours may apply between Christmas and New Year's Day.
2. Membership & Library Cards
Anyone who lives, works, attends school, ...
  3. [Doc ID: 28] s.
1.2 Eastside Branch
The Eastside Branch, located at 47 Birchwood Avenue, is open Monday through Friday from 10:00 AM to 6:00
PM and Saturday from 1...

**Question 17:** What does the document state regarding: All branches are closed on major public holidays, including New Year's Day, Independence D?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** ay, Independence Day, Thanksgiving,
and Christmas Day.
1.1 Main Branch
The Main Branch, located at 123 Elm Street, is open Monday through Thursday from 9:00 AM to 8:00 PM,
Friday from 9:00 AM to 6:00 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] ay, Independence Day, Thanksgiving,
and Christmas Day.
1.1 Main Branch
The Main Branch, located at 123 Elm Street, is open Monday through Thursday fro...
  2. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...
  3. [Doc ID: 28] 
In addition to standard weekly hours, all branches close early at 2:00 PM on the day before Thanksgiving and
Christmas Eve. Members should check the ...

**Question 18:** What does the document state regarding: 2 Card Renewal Library cards must be renewed every three years?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 29]  items checked out on a lost card before it is
reported.
3. Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & ...
  3. [Doc ID: 29] son at any branch or online
through the library's account portal, provided contact information is current.
2.3 Lost or Stolen Cards
A lost or stolen c...

**Question 19:** What does the document state regarding: Members will receive an email reminder 30 days before expiration if an email address is on?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 30] d Items
If an item is not returned within 30 days of its due date, it is considered lost and the member's account is
charged the item's full replaceme...
  3. [Doc ID: 29] als can be completed online, by phone, or in person, provided no other member has placed a hold on
the item. Items with active holds cannot be renewed...

**Question 20:** What does the document state regarding: 1 Overdue Fines Riverbend Public Library uses a fine-free model for standard books, audiob?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines s...
  2. [Doc ID: 29] ested through interlibrary loan from partner
systems. Requests typically take 5 to 14 business days to arrive. Interlibrary loan items follow the lend...
  3. [Doc ID: 29] is kept on the hold shelf for 7
days before being returned to circulation or passed to the next person in the queue.
3.3 Interlibrary Loan
Items not o...

**Question 21:** What does the document state regarding: However, overdue fines still apply to high-demand items: DVDs and video games accrue $0?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines s...
  2. [Doc ID: 30] mes accrue $0.50 per day, up to a
maximum of $10.00 per item. Library-owned laptops and hotspots accrue $5.00 per day, with no maximum cap,
reflecting...
  3. [Doc ID: 30] d Items
If an item is not returned within 30 days of its due date, it is considered lost and the member's account is
charged the item's full replaceme...

**Question 22:** What does the document state regarding: The catalog below reflects a sample of frequently requested titles across genres, current ?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 31] ibrarian for real-time
status.
6.1 Fantasy & Science Fiction
Title
Author
Format
Copies
Harry Potter and the Sorcerer's Stone
J.K. Rowling
Book / Audi...
  3. [Doc ID: 31]  the Wind
Patrick Rothfuss
Book
2
Mistborn: The Final Empire
Brandon Sanderson
Book / Audiobook
3
6.2 Mystery & Thriller
Title
Author
Format
Copies
Th...

**Question 23:** What does the document state regarding: Availability changes daily; members should check the online catalog or ask a librarian for?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 29] als can be completed online, by phone, or in person, provided no other member has placed a hold on
the item. Items with active holds cannot be renewed...
  3. [Doc ID: 29]  Reservations
Members may place holds on items that are currently checked out or located at another branch. A member may
have up to 15 active holds at...

**Question 24:** What does the document state regarding: Palacio Book / E-book 4 The Fault in Our Stars John Green Book / Audiobook 3 Charlotte's W?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7. Programs & Events
7.1 Storytime & Children's Programs
Storytime for ages 2...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7. Programs & Events
7.1 St...
  2. [Doc ID: 31] ibrarian for real-time
status.
6.1 Fantasy & Science Fiction
Title
Author
Format
Copies
Harry Potter and the Sorcerer's Stone
J.K. Rowling
Book / Audi...
  3. [Doc ID: 31] dult
Title
Author
Format
Copies
Percy Jackson and the Lightning Thief
Rick Riordan
Book / Audiobook
5...

**Question 25:** What does the document state regarding: Programs & Events 7?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:**  runs monthly on the first Tuesday at the Eastside Branch.
7.2 Adult Programs
The Main Branch hosts a monthly book club on the second Thursday evening at 6:30 PM, rotating between
fiction and nonficti...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32]  runs monthly on the first Tuesday at the Eastside Branch.
7.2 Adult Programs
The Main Branch hosts a monthly book club on the second Thursday evening...
  2. [Doc ID: 32] on selections chosen by member vote. A local history lecture series runs quarterly at the Main
Branch, drawing on the library's archive collection.
7....
  3. [Doc ID: 23] ercial, non-sectarian, and of general community interest. Postings are limited to 30 days....

**Question 26:** What does the document state regarding: Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibra?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict certain
items, such as rare books or current bests...
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  2. [Doc ID: 10] s for a book to arrive. Loan periods are set by the lending library....
  3. [Doc ID: 29]  Reservations
Members may place holds on items that are currently checked out or located at another branch. A member may
have up to 15 active holds at...

**Question 27:** What does the document state regarding: Some lending libraries restrict certain items, such as rare books or current bestsellers, ?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict certain
items, such as rare books or current bests...
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  2. [Doc ID: 10] s for a book to arrive. Loan periods are set by the lending library....
  3. [Doc ID: 29] erbend's standard loan periods.
4. Fines, Fees & Lost Items...

### Config 2: Fixed-Size Large (Dense)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...
  3. [Doc ID: 32] by name on your account, or if the item is not marked confidential.
Confidential holds can only be picked up by the account holder with photo ID.
Do y...

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 16] Patrons may bring covered drinks and small snacks into the library. Hot food, meals, and messy snacks are not allowed in the study areas. Please dispo...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 8] The children's section is designed for kids under 12 years old. Storytime sessions are held every Tuesday and Thursday morning starting at 10:30 AM. P...
  3. [Doc ID: 28] branch specializes in children's and
young adult collections and hosts weekly storytime sessions on Wednesday mornings at 10:30 AM.
1.3 Riverside Bran...

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  3. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 25] We are committed to protecting your privacy. The library does not disclose information about borrowed books, search histories, or personal details to ...
  3. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside the library or the external drop box located next ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...
  2. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...
  3. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines s...

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Materials must be returned in the same condition they were...
- **Retrieved Chunks Order:**
  1. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Material...
  2. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...
  3. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance. We accept fiction...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may purchase an annual membership.
2.1 Membership Tiers...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 32] by name on your account, or if the item is not marked confidential.
Confidential holds can only be picked up by the account holder with photo ID.
Do y...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued photo ID along with proof of address (such as a utili...
- **Retrieved Chunks Order:**
  1. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  2. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...
  3. [Doc ID: 32] by name on your account, or if the item is not marked confidential.
Confidential holds can only be picked up by the account holder with photo ID.
Do y...

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict certain
items, such as rare books or current bests...
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

**Question 12:** What object does Bilbo find on his journey that becomes important later?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical world of Middle-earth. The story follows the quest of...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  2. [Doc ID: 13] Items found in the library are turned in to the front desk. Valuable items such as phones, wallets, and keys are kept in a secure locker. Unclaimed it...
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851. It details the voyage of the whaling ship Pequod, commanded by Captain Ah...

**Question 13:** Which mountain do the dwarves want to reclaim from the dragon?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical world of Middle-earth. The story follows the quest of...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  2. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  3. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 20] A Brief History of Time is a popular-science book written by English physicist Stephen Hawking. First published in 1988, it explains complex topics in...
  3. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...

**Question 15:** What does the document state regarding: Riverbend Public Library Member Handbook & Policy Guide Effective 2026 Edition 123 Elm Str?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  2. [Doc ID: 28] branch specializes in children's and
young adult collections and hosts weekly storytime sessions on Wednesday mornings at 10:30 AM.
1.3 Riverside Bran...
  3. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...

**Question 16:** What does the document state regarding: Hours & Locations Riverbend Public Library operates three branches across the city, each w?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed on major public holidays, including New Year's D...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...
  2. [Doc ID: 28] branch specializes in children's and
young adult collections and hosts weekly storytime sessions on Wednesday mornings at 10:30 AM.
1.3 Riverside Bran...
  3. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...

**Question 17:** What does the document state regarding: All branches are closed on major public holidays, including New Year's Day, Independence D?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed on major public holidays, including New Year's D...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are close...
  2. [Doc ID: 28] branch specializes in children's and
young adult collections and hosts weekly storytime sessions on Wednesday mornings at 10:30 AM.
1.3 Riverside Bran...
  3. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...

**Question 18:** What does the document state regarding: 2 Card Renewal Library cards must be renewed every three years?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...
  3. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...

**Question 19:** What does the document state regarding: Members will receive an email reminder 30 days before expiration if an email address is on?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...
  3. [Doc ID: 28] le for a free library
card. Proof of address, such as a driver's license, utility bill, or lease agreement, is required at signup.
Non-residents may p...

**Question 20:** What does the document state regarding: 1 Overdue Fines Riverbend Public Library uses a fine-free model for standard books, audiob?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines s...
  2. [Doc ID: 29] ested through interlibrary loan from partner
systems. Requests typically take 5 to 14 business days to arrive. Interlibrary loan items follow the lend...
  3. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...

**Question 21:** What does the document state regarding: However, overdue fines still apply to high-demand items: DVDs and video games accrue $0?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024.
However, overdue fines s...
  2. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...
  3. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...

**Question 22:** What does the document state regarding: The catalog below reflects a sample of frequently requested titles across genres, current ?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 28] branch specializes in children's and
young adult collections and hosts weekly storytime sessions on Wednesday mornings at 10:30 AM.
1.3 Riverside Bran...
  3. [Doc ID: 31] 
4
Gone Girl
Gillian Flynn
Book / E-book
3
The Thursday Murder Club
Richard Osman
Book / Audiobook
3
Big Little Lies
Liane Moriarty
Book
2
6.3 Nonfict...

**Question 23:** What does the document state regarding: Availability changes daily; members should check the online catalog or ask a librarian for?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 30] cally 14 or 21 days depending on the title, and items are returned
automatically at the end of the loan period with no late fees possible. The library...

**Question 24:** What does the document state regarding: Palacio Book / E-book 4 The Fault in Our Stars John Green Book / Audiobook 3 Charlotte's W?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7. Programs & Events
7.1 Storytime & Children's Programs
Storytime for ages 2...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7. Programs & Events
7.1 St...
  2. [Doc ID: 31] 
4
Gone Girl
Gillian Flynn
Book / E-book
3
The Thursday Murder Club
Richard Osman
Book / Audiobook
3
Big Little Lies
Liane Moriarty
Book
2
6.3 Nonfict...
  3. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...

**Question 25:** What does the document state regarding: Programs & Events 7?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7. Programs & Events
7.1 Storytime & Children's Programs
Storytime for ages 2...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7. Programs & Events
7.1 St...
  2. [Doc ID: 28] branch specializes in children's and
young adult collections and hosts weekly storytime sessions on Wednesday mornings at 10:30 AM.
1.3 Riverside Bran...
  3. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...

**Question 26:** What does the document state regarding: Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibra?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict certain
items, such as rare books or current bests...
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 29] ested through interlibrary loan from partner
systems. Requests typically take 5 to 14 business days to arrive. Interlibrary loan items follow the lend...

**Question 27:** What does the document state regarding: Some lending libraries restrict certain items, such as rare books or current bestsellers, ?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict certain
items, such as rare books or current bests...
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests?
Members may have up to 5 active interlibrary loan requests at a time. Some lending libraries restrict ...
  2. [Doc ID: 30] smoke, or pet damage are billed at full replacement
cost regardless of when they are returned.
4.3 Account Blocks
Accounts with more than $25.00 in un...
  3. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Material...

### Config 3: Semantic (Dense)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
  3. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announceme...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  2. [Doc ID: 9] If a room is not occupied within 15 minutes of the start time, the booking is cancelled....
  3. [Doc ID: 22] A fee of $25 per hour applies....

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 33] Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  2. [Doc ID: 26] Materials must be returned in the same condition they were borrowed. Repeat offenders may have their borrowing privileges suspended....
  3. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ❌ No (Expected Doc ID: 3)
- **Answer Produced:** A fee of $25 per hour applies....
- **Retrieved Chunks Order:**
  1. [Doc ID: 22] A fee of $25 per hour applies....
  2. [Doc ID: 29] 4. Fines, Fees & Lost Items...
  3. [Doc ID: 9] If a room is not occupied within 15 minutes of the start time, the booking is cancelled....

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** Materials must be returned in the same condition they were borrowed. Repeat offenders may have their borrowing privileges suspended....
- **Retrieved Chunks Order:**
  1. [Doc ID: 26] Materials must be returned in the same condition they were borrowed. Repeat offenders may have their borrowing privileges suspended....
  2. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
  3. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage....

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
- **Retrieved Chunks Order:**
  1. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** We are committed to protecting your privacy....
- **Retrieved Chunks Order:**
  1. [Doc ID: 25] We are committed to protecting your privacy....
  2. [Doc ID: 23] Postings are limited to 30 days....
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 25] We are committed to protecting your privacy....
  3. [Doc ID: 8] The children's section is designed for kids under 12 years old....

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
  2. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....
  3. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...

**Question 12:** What object does Bilbo find on his journey that becomes important later?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  2. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  3. [Doc ID: 13] Items found in the library are turned in to the front desk....

**Question 13:** Which mountain do the dwarves want to reclaim from the dragon?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical world of Middle-earth. The story follows the quest of...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 28] 1....

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 6] The novel explores themes of politics, religion, ecology, and human power. Paul must navigate betrayal, lead the indigenous Fremen people, and fulfill...
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851....

**Question 15:** What does the document state regarding: Riverbend Public Library Member Handbook & Policy Guide Effective 2026 Edition 123 Elm Str?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  2. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 16:** What does the document state regarding: Hours & Locations Riverbend Public Library operates three branches across the city, each w?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed on major public holidays, including New Year's Day,...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...
  2. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...
  3. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...

**Question 17:** What does the document state regarding: All branches are closed on major public holidays, including New Year's Day, Independence D?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announceme...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  2. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...
  3. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...

**Question 18:** What does the document state regarding: 2 Card Renewal Library cards must be renewed every three years?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...
  3. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...

**Question 19:** What does the document state regarding: Members will receive an email reminder 30 days before expiration if an email address is on?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 23] Postings are limited to 30 days....
  3. [Doc ID: 25] We are committed to protecting your privacy....

**Question 20:** What does the document state regarding: 1 Overdue Fines Riverbend Public Library uses a fine-free model for standard books, audiob?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 21:** What does the document state regarding: However, overdue fines still apply to high-demand items: DVDs and video games accrue $0?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  2. [Doc ID: 29] 4. Fines, Fees & Lost Items...
  3. [Doc ID: 26] Materials must be returned in the same condition they were borrowed. Repeat offenders may have their borrowing privileges suspended....

**Question 22:** What does the document state regarding: The catalog below reflects a sample of frequently requested titles across genres, current ?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 31] 6.1 Fantasy & Science Fiction
Title
Author
Format
Copies
Harry Potter and the Sorcerer's Stone
J.K. Rowling
Book / Audiobook / E-book
6
Harry Potter a...
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 23:** What does the document state regarding: Availability changes daily; members should check the online catalog or ask a librarian for?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...
  3. [Doc ID: 33] Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....

**Question 24:** What does the document state regarding: Palacio Book / E-book 4 The Fault in Our Stars John Green Book / Audiobook 3 Charlotte's W?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7....
  2. [Doc ID: 31] 6.1 Fantasy & Science Fiction
Title
Author
Format
Copies
Harry Potter and the Sorcerer's Stone
J.K. Rowling
Book / Audiobook / E-book
6
Harry Potter a...
  3. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...

**Question 25:** What does the document state regarding: Programs & Events 7?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** A separate baby-and-me lapsit session for children
under 2 runs monthly on the first Tuesday at the Eastside Branch. 7.2 Adult Programs
The Main Branch hosts a monthly book club on the second Thursday...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] A separate baby-and-me lapsit session for children
under 2 runs monthly on the first Tuesday at the Eastside Branch. 7.2 Adult Programs
The Main Branc...
  2. [Doc ID: 30] 5....
  3. [Doc ID: 32] Programs & Events
7.1 Storytime & Children's Programs
Storytime for ages 2 to 5 runs every Wednesday at 10:30 AM at the Eastside Branch and every Satu...

**Question 26:** What does the document state regarding: Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibra?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
  2. [Doc ID: 33] Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 27:** What does the document state regarding: Some lending libraries restrict certain items, such as rare books or current bestsellers, ?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

### Config 4: Semantic (Hybrid RRF)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announceme...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  3. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 21] Free parking is available for all library visitors in the north parking lot. Patrons must display a valid parking permit on their dashboard if parking...
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** 8. Frequently Asked Questions
Can I return items to any branch? Yes....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  2. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  3. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
  2. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
- **Retrieved Chunks Order:**
  1. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
  2. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** 8. Frequently Asked Questions
Can I return items to any branch? Yes....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  2. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 25] We are committed to protecting your privacy....

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** 8. Frequently Asked Questions
Can I return items to any branch? Yes....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  2. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...
  3. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...

**Question 12:** What object does Bilbo find on his journey that becomes important later?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  2. [Doc ID: 17] It details the voyage of the whaling ship Pequod, commanded by Captain Ahab. Ahab is obsessed with seeking revenge on Moby Dick, a giant white sperm w...
  3. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...

**Question 13:** Which mountain do the dwarves want to reclaim from the dragon?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical world of Middle-earth. The story follows the quest of...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 32] Items borrowed from any Riverbend branch may be returned to any of the three branches, or deposited in
the exterior book drop, which is checked daily ...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851....

**Question 15:** What does the document state regarding: Riverbend Public Library Member Handbook & Policy Guide Effective 2026 Edition 123 Elm Str?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  2. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 16:** What does the document state regarding: Hours & Locations Riverbend Public Library operates three branches across the city, each w?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed on major public holidays, including New Year's Day,...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...
  2. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 17:** What does the document state regarding: All branches are closed on major public holidays, including New Year's Day, Independence D?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announceme...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  2. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...
  3. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...

**Question 18:** What does the document state regarding: 2 Card Renewal Library cards must be renewed every three years?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...

**Question 19:** What does the document state regarding: Members will receive an email reminder 30 days before expiration if an email address is on?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 9] If a room is not occupied within 15 minutes of the start time, the booking is cancelled....
  3. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...

**Question 20:** What does the document state regarding: 1 Overdue Fines Riverbend Public Library uses a fine-free model for standard books, audiob?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...

**Question 21:** What does the document state regarding: However, overdue fines still apply to high-demand items: DVDs and video games accrue $0?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 22:** What does the document state regarding: The catalog below reflects a sample of frequently requested titles across genres, current ?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 33] Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
  3. [Doc ID: 25] The library does not disclose information about borrowed books, search histories, or personal details to third parties unless required by law. Patron ...

**Question 23:** What does the document state regarding: Availability changes daily; members should check the online catalog or ask a librarian for?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...
  3. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...

**Question 24:** What does the document state regarding: Palacio Book / E-book 4 The Fault in Our Stars John Green Book / Audiobook 3 Charlotte's W?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7....
  2. [Doc ID: 31] 6.1 Fantasy & Science Fiction
Title
Author
Format
Copies
Harry Potter and the Sorcerer's Stone
J.K. Rowling
Book / Audiobook / E-book
6
Harry Potter a...
  3. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...

**Question 25:** What does the document state regarding: Programs & Events 7?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** A separate baby-and-me lapsit session for children
under 2 runs monthly on the first Tuesday at the Eastside Branch. 7.2 Adult Programs
The Main Branch hosts a monthly book club on the second Thursday...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] A separate baby-and-me lapsit session for children
under 2 runs monthly on the first Tuesday at the Eastside Branch. 7.2 Adult Programs
The Main Branc...
  2. [Doc ID: 32] Programs & Events
7.1 Storytime & Children's Programs
Storytime for ages 2 to 5 runs every Wednesday at 10:30 AM at the Eastside Branch and every Satu...
  3. [Doc ID: 29] 4. Fines, Fees & Lost Items...

**Question 26:** What does the document state regarding: Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibra?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
  2. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...
  3. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...

**Question 27:** What does the document state regarding: Some lending libraries restrict certain items, such as rare books or current bestsellers, ?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage....

### Config 5: Semantic (Hybrid + Reranker)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announceme...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  3. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 21] Free parking is available for all library visitors in the north parking lot. Patrons must display a valid parking permit on their dashboard if parking...
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** 8. Frequently Asked Questions
Can I return items to any branch? Yes....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  2. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  3. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
  2. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
- **Retrieved Chunks Order:**
  1. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
  2. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** 8. Frequently Asked Questions
Can I return items to any branch? Yes....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  2. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 25] We are committed to protecting your privacy....

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** 8. Frequently Asked Questions
Can I return items to any branch? Yes....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] 8. Frequently Asked Questions
Can I return items to any branch? Yes....
  2. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...
  3. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...

**Question 12:** What object does Bilbo find on his journey that becomes important later?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  2. [Doc ID: 17] It details the voyage of the whaling ship Pequod, commanded by Captain Ahab. Ahab is obsessed with seeking revenge on Moby Dick, a giant white sperm w...
  3. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...

**Question 13:** Which mountain do the dwarves want to reclaim from the dragon?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical world of Middle-earth. The story follows the quest of...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 32] Items borrowed from any Riverbend branch may be returned to any of the three branches, or deposited in
the exterior book drop, which is checked daily ...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851....

**Question 15:** What does the document state regarding: Riverbend Public Library Member Handbook & Policy Guide Effective 2026 Edition 123 Elm Str?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  2. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 16:** What does the document state regarding: Hours & Locations Riverbend Public Library operates three branches across the city, each w?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed on major public holidays, including New Year's Day,...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...
  2. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...
  3. [Doc ID: 28] Membership & Library Cards
Anyone who lives, works, attends school, or owns property within Riverbend County is eligible for a free library
card. Proo...

**Question 17:** What does the document state regarding: All branches are closed on major public holidays, including New Year's Day, Independence D?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM. Please check the website for real-time announceme...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  2. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...
  3. [Doc ID: 28] Hours & Locations
Riverbend Public Library operates three branches across the city, each with its own schedule and services. All
branches are closed o...

**Question 18:** What does the document state regarding: 2 Card Renewal Library cards must be renewed every three years?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...

**Question 19:** What does the document state regarding: Members will receive an email reminder 30 days before expiration if an email address is on?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address is on file. An expired card can be renewed in per...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] 2.2 Card Renewal
Library cards must be renewed every three years. Members will receive an email reminder 30 days before
expiration if an email address...
  2. [Doc ID: 9] If a room is not occupied within 15 minutes of the start time, the booking is cancelled....
  3. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...

**Question 20:** What does the document state regarding: 1 Overdue Fines Riverbend Public Library uses a fine-free model for standard books, audiob?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 27] Riverbend Public Library
Member Handbook & Policy Guide
Effective 2026 Edition
123 Elm Street, Riverbend, IL 62901...

**Question 21:** What does the document state regarding: However, overdue fines still apply to high-demand items: DVDs and video games accrue $0?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines still apply to high-demand items: DVDs and video ga...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...
  2. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 22:** What does the document state regarding: The catalog below reflects a sample of frequently requested titles across genres, current ?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 33] Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
  3. [Doc ID: 25] The library does not disclose information about borrowed books, search histories, or personal details to third parties unless required by law. Patron ...

**Question 23:** What does the document state regarding: Availability changes daily; members should check the online catalog or ask a librarian for?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; members should check the online catalog or ask a l...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] The catalog below reflects a sample of frequently requested titles across genres, current as of this handbook's
printing. Availability changes daily; ...
  2. [Doc ID: 28] This branch focuses on periodicals, digital media, and a dedicated quiet
study floor. 1.4 Holiday Closures
In addition to standard weekly hours, all b...
  3. [Doc ID: 30] Digital Resources & Facilities
5.1 E-books & Streaming
Members can borrow e-books and audiobooks through the library's digital lending app using their...

**Question 24:** What does the document state regarding: Palacio Book / E-book 4 The Fault in Our Stars John Green Book / Audiobook 3 Charlotte's W?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Wonder
R.J. Palacio
Book / E-book
4
The Fault in Our Stars
John Green
Book / Audiobook
3
Charlotte's Web
E.B. White
Book
6
7....
  2. [Doc ID: 31] 6.1 Fantasy & Science Fiction
Title
Author
Format
Copies
Harry Potter and the Sorcerer's Stone
J.K. Rowling
Book / Audiobook / E-book
6
Harry Potter a...
  3. [Doc ID: 30] 4.1 Overdue Fines
Riverbend Public Library uses a fine-free model for standard books, audiobooks, and periodicals as of 2024. However, overdue fines s...

**Question 25:** What does the document state regarding: Programs & Events 7?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** A separate baby-and-me lapsit session for children
under 2 runs monthly on the first Tuesday at the Eastside Branch. 7.2 Adult Programs
The Main Branch hosts a monthly book club on the second Thursday...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] A separate baby-and-me lapsit session for children
under 2 runs monthly on the first Tuesday at the Eastside Branch. 7.2 Adult Programs
The Main Branc...
  2. [Doc ID: 32] Programs & Events
7.1 Storytime & Children's Programs
Storytime for ages 2 to 5 runs every Wednesday at 10:30 AM at the Eastside Branch and every Satu...
  3. [Doc ID: 29] 4. Fines, Fees & Lost Items...

**Question 26:** What does the document state regarding: Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibra?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Is there a limit on interlibrary loan requests? Members may have up to 5 active interlibrary loan requests at a time....
  2. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...
  3. [Doc ID: 29] Borrowing Policies
3.1 Loan Periods
Item Type
Loan Period
Renewals Allowed
Books (adult & YA)
21 days
2 renewals
Children's books
21 days
2 renewals
D...

**Question 27:** What does the document state regarding: Some lending libraries restrict certain items, such as rare books or current bestsellers, ?

- **Hit:** ✅ Yes (Expected Doc ID: 33)
- **Answer Produced:** Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
- **Retrieved Chunks Order:**
  1. [Doc ID: 33] Some lending libraries restrict certain
items, such as rare books or current bestsellers, from interlibrary loan entirely....
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage....

