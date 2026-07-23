# RAG Evaluation Comparison Report

This report compares the impact of 5 retrieval configurations on the retrieval of relevant chunks and final answers.

## Configuration Summary & Hit Rates

| Config | Strategy | Chunk Size | Overlap | Top K | Hybrid | Reranker | Hit Rate | Precision | Recall | F1 Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Config 1: Fixed-Size Small (Dense)** | fixed | 250 | 50 | 3 | False | False | **92.0%** | 0.31 | 0.92 | 0.46 |
| **Config 2: Fixed-Size Large (Dense)** | fixed | 1000 | 200 | 3 | False | False | **96.0%** | 0.32 | 0.96 | 0.48 |
| **Config 3: Semantic (Dense)** | semantic | auto | auto | 3 | False | False | **84.0%** | 0.28 | 0.84 | 0.42 |
| **Config 4: Semantic (Hybrid RRF)** | semantic | auto | auto | 3 | True | False | **100.0%** | 0.33 | 1.00 | 0.50 |
| **Config 5: Semantic (Hybrid + Reranker)** | semantic | auto | auto | 3 | True | True | **100.0%** | 0.33 | 1.00 | 0.50 |

---

## Detailed Query Logs

Below is the breakdown of exactly which chunks were retrieved, in what order, and what answer was produced for each query under each configuration.

### Config 1: Fixed-Size Small (Dense)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 1] until midnight. Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually c...
  3. [Doc ID: 1] n Saturdays, we operate on reduced hours, opening at 10:00 AM and closing at 6:00 PM. The library is closed on Sundays to allow for deep cleaning and ...

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** n Saturdays, we operate on reduced hours, opening at 10:00 AM and closing at 6:00 PM. The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] n Saturdays, we operate on reduced hours, opening at 10:00 AM and closing at 6:00 PM. The library is closed on Sundays to allow for deep cleaning and ...
  2. [Doc ID: 28]  to standard hours once exams conclude.
1.2 Whitfield Research Annex
Open Monday through Friday from 8:00 AM to 9:00 PM and Saturday from 10:00 AM to ...
  3. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...

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
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** ested online, via our mobile app, or at the front desk. Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] ested online, via our mobile app, or at the front desk. Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 32] ent students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private rooms.
How do I access journal databases f...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligible
Items unreturned 45 days past the due date are...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligi...
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
  3. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** nterested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] nterested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 4] ty bill or student card). Students enrolled in the local university receive automatic membership using their student ID card. Once registered, members...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** nterested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] nterested individuals must fill out an application and pass a background check....
  2. [Doc ID: 25] ds are kept strictly confidential and are only accessed by authorized staff members....
  3. [Doc ID: 31] t
no cost for the first year after graduation, and at the standard $60 annual fee thereafter.
What happens to my loans over the summer?...

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** r digital access. The digital library provides access to over 10,000 e-books and academic journals. Do not share your library card or PIN; members are responsible for all items checked out under their...
- **Retrieved Chunks Order:**
  1. [Doc ID: 4] r digital access. The digital library provides access to over 10,000 e-books and academic journals. Do not share your library card or PIN; members are...
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 10] s for a book to arrive. Loan periods are set by the lending library....

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

**Question 15:** What does the document state regarding: Maple Hill University Library System Graduate & Undergraduate Services Guide 2026-2027 Aca?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01760...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...
  2. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  3. [Doc ID: 29] s depending on item type, and equipment
cannot be renewed if another reservation is pending.
5. Interlibrary Loan & Consortium Borrowing
Maple Hill Un...

**Question 16:** What does the document state regarding: Library Access & Hours Maple Hill University Library operates two main facilities: the Cal?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 28] ulty, and archival research. Access to both
requires a valid MHU ID card, tapped at the turnstile entrance.
1.1 Callahan Library
Open Monday through T...
  3. [Doc ID: 29] s depending on item type, and equipment
cannot be renewed if another reservation is pending.
5. Interlibrary Loan & Consortium Borrowing
Maple Hill Un...

**Question 17:** What does the document state regarding: Access to both requires a valid MHU ID card, tapped at the turnstile entrance?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** ulty, and archival research. Access to both
requires a valid MHU ID card, tapped at the turnstile entrance.
1.1 Callahan Library
Open Monday through Thursday from 7:00 AM to 2:00 AM, Friday from 7:00 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] ulty, and archival research. Access to both
requires a valid MHU ID card, tapped at the turnstile entrance.
1.1 Callahan Library
Open Monday through T...
  2. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  3. [Doc ID: 25] ds are kept strictly confidential and are only accessed by authorized staff members....

**Question 18:** What does the document state regarding: student, faculty, or staff request?

- **Hit:** ❌ No (Expected Doc ID: 29)
- **Answer Produced:** ds are kept strictly confidential and are only accessed by authorized staff members....
- **Retrieved Chunks Order:**
  1. [Doc ID: 25] ds are kept strictly confidential and are only accessed by authorized staff members....
  2. [Doc ID: 32] ject to
copyright compliance review, typically completed within 3 to 5 business days of the request.
Are group study rooms available to community borr...
  3. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...

**Question 19:** What does the document state regarding: Faculty loans on course reserve materials are exempt from recall during the semester in wh?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught.
3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 29] ulation desk.
3.3 Course Reserves
Instructors may place materials on 2-hour, 24-hour, or 3-day reserve loan periods for a specific course. Reserve
mat...
  3. [Doc ID: 29] online through the library catalog, provided no recall or hold has been
placed. Items already overdue by more than 7 days cannot be renewed online and...

**Question 20:** What does the document state regarding: 1 Group Study Rooms Callahan Library offers 14 group study rooms bookable up to 7 days in ?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 30] graduate-only study rooms, bookable up to
14 days in advance, reflecting longer typical research sessions.
6.2 Silent Floors
The third and fourth floo...
  3. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...

**Question 21:** What does the document state regarding: The Whitfield Annex offers 4 graduate-only study rooms, bookable up to 14 days in advance,?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 30]  floors, where conversation, phone
calls, and group work are prohibited. The entire Whitfield Annex operates under a silent-by-default policy
outside ...

**Question 22:** What does the document state regarding: A People's History of the United States Howard Zinn Book / E-book 5 The Structure of Scien?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 31] / Audiobook
4
7.4 Life & Physical Sciences
Title
Author
Format
Copies
Campbell Biology
Urry, Cain, Wasserman, et al.
Book / Reserve
9
Organic Chemistr...
  3. [Doc ID: 31] ics for People in a Hurry
Neil deGrasse Tyson
Book / Audiobook
3
Principles of Neural Science
Kandel, Schwartz, Jessell
Book / Reserve
5
8. Research S...

**Question 23:** What does the document state regarding: 4 Life & Physical Sciences Title Author Format Copies Campbell Biology Urry, Cain, Wasserm?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** / Audiobook
4
7.4 Life & Physical Sciences
Title
Author
Format
Copies
Campbell Biology
Urry, Cain, Wasserman, et al.
Book / Reserve
9
Organic Chemistry
Paula Yurkanis Bruice
Book / Reserve
7
Astrophys...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] / Audiobook
4
7.4 Life & Physical Sciences
Title
Author
Format
Copies
Campbell Biology
Urry, Cain, Wasserman, et al.
Book / Reserve
9
Organic Chemistr...
  2. [Doc ID: 30] 
The Lean Startup
Eric Ries
Book / E-book
4
Corporate Finance
Ross, Westerfield, Jaffe
Book / Reserve
6
7.3 Humanities & Social Sciences
Title
Author
...
  3. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...

**Question 24:** What does the document state regarding: Undergraduate and graduate loan periods automatically extend through the summer term for a?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 31] t
no cost for the first year after graduation, and at the standard $60 annual fee thereafter.
What happens to my loans over the summer?...
  3. [Doc ID: 28] 0 AM to 6:00 PM) during winter break and spring break. The
library is fully closed during the week between Christmas and New Year's Day, and on all fe...

**Question 25:** What does the document state regarding: Can I request a course reserve item be scanned instead of checked out? Instructors can req?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** for the
following fall term.
Can I request a course reserve item be scanned instead of checked out?
Instructors can request short excerpts be digitized and placed on the electronic reserve system, sub...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] for the
following fall term.
Can I request a course reserve item be scanned instead of checked out?
Instructors can request short excerpts be digitize...
  2. [Doc ID: 29] ulation desk.
3.3 Course Reserves
Instructors may place materials on 2-hour, 24-hour, or 3-day reserve loan periods for a specific course. Reserve
mat...
  3. [Doc ID: 29] oan and must be returned to the reserve desk, not the
general book drop.
4. Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergra...

### Config 2: Fixed-Size Large (Dense)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...
  3. [Doc ID: 21] Free parking is available for all library visitors in the north parking lot. Patrons must display a valid parking permit on their dashboard if parking...

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  3. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 8] The children's section is designed for kids under 12 years old. Storytime sessions are held every Tuesday and Thursday morning starting at 10:30 AM. P...
  3. [Doc ID: 21] Free parking is available for all library visitors in the north parking lot. Patrons must display a valid parking permit on their dashboard if parking...

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 28] s on items needed for thesis, dissertation, or active
grant-funded research by submitting an extended loan form to their subject librarian. Community ...

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 25] We are committed to protecting your privacy. The library does not disclose information about borrowed books, search histories, or personal details to ...
  3. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Material...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside the library or the external drop box located next ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...
  2. [Doc ID: 29] uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligi...
  3. [Doc ID: 28] s on items needed for thesis, dissertation, or active
grant-funded research by submitting an extended loan form to their subject librarian. Community ...

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Materials must be returned in the same condition they were...
- **Retrieved Chunks Order:**
  1. [Doc ID: 26] Patrons are expected to treat all library materials with care. Highlighting, writing, or folding pages in library books is considered damage. Material...
  2. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...
  3. [Doc ID: 25] We are committed to protecting your privacy. The library does not disclose information about borrowed books, search histories, or personal details to ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...
  3. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance. We accept fiction...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued photo ID along with proof of address (such as a utili...
- **Retrieved Chunks Order:**
  1. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  2. [Doc ID: 25] We are committed to protecting your privacy. The library does not disclose information about borrowed books, search histories, or personal details to ...
  3. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued photo ID along with proof of address (such as a utili...
- **Retrieved Chunks Order:**
  1. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  2. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  3. [Doc ID: 12] The library offers volunteer opportunities for teens and adults. Volunteers help with shelving books, organizing events, and assisting patrons. High s...

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 25] We are committed to protecting your privacy. The library does not disclose information about borrowed books, search histories, or personal details to ...

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
  2. [Doc ID: 25] We are committed to protecting your privacy. The library does not disclose information about borrowed books, search histories, or personal details to ...
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851. It details the voyage of the whaling ship Pequod, commanded by Captain Ah...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 20] A Brief History of Time is a popular-science book written by English physicist Stephen Hawking. First published in 1988, it explains complex topics in...
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851. It details the voyage of the whaling ship Pequod, commanded by Captain Ah...

**Question 15:** What does the document state regarding: Maple Hill University Library System Graduate & Undergraduate Services Guide 2026-2027 Aca?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01760...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...
  2. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  3. [Doc ID: 29] uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligi...

**Question 16:** What does the document state regarding: Library Access & Hours Maple Hill University Library operates two main facilities: the Cal?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 29] uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligi...
  3. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...

**Question 17:** What does the document state regarding: Access to both requires a valid MHU ID card, tapped at the turnstile entrance?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 29] uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligi...
  3. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...

**Question 18:** What does the document state regarding: student, faculty, or staff request?

- **Hit:** ❌ No (Expected Doc ID: 29)
- **Answer Produced:** ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Schedule
Both facilities operate on reduced hours (10:0...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...
  2. [Doc ID: 28] s on items needed for thesis, dissertation, or active
grant-funded research by submitting an extended loan form to their subject librarian. Community ...
  3. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...

**Question 19:** What does the document state regarding: Faculty loans on course reserve materials are exempt from recall during the semester in wh?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught.
3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 28] s on items needed for thesis, dissertation, or active
grant-funded research by submitting an extended loan form to their subject librarian. Community ...
  3. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...

**Question 20:** What does the document state regarding: 1 Group Study Rooms Callahan Library offers 14 group study rooms bookable up to 7 days in ?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 21:** What does the document state regarding: The Whitfield Annex offers 4 graduate-only study rooms, bookable up to 14 days in advance,?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 22:** What does the document state regarding: A People's History of the United States Howard Zinn Book / E-book 5 The Structure of Scien?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 5 per color page. 3D printing services are available
at the Callahan Library makerspace by appointment, billed by gram of material used.
7. Collection...
  3. [Doc ID: 28] s on items needed for thesis, dissertation, or active
grant-funded research by submitting an extended loan form to their subject librarian. Community ...

**Question 23:** What does the document state regarding: 4 Life & Physical Sciences Title Author Format Copies Campbell Biology Urry, Cain, Wasserm?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 5 per color page. 3D printing services are available
at the Callahan Library makerspace by appointment, billed by gram of material used.
7. Collection...
  3. [Doc ID: 29] uate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall applies
N/A
$5.00/day
Community Borrower
$0.50/day, $20 max
N/A
Not eligi...

**Question 24:** What does the document state regarding: Undergraduate and graduate loan periods automatically extend through the summer term for a?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 28] ripts reading room within the Annex requires an appointment booked at
least 48 hours in advance through the archives office.
1.3 Break & Holiday Sched...
  3. [Doc ID: 28] s on items needed for thesis, dissertation, or active
grant-funded research by submitting an extended loan form to their subject librarian. Community ...

**Question 25:** What does the document state regarding: Can I request a course reserve item be scanned instead of checked out? Instructors can req?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 29] sortium, granting students and faculty direct
borrowing privileges at 11 partner university libraries across the state. Consortium items are requested...

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
  3. [Doc ID: 31] Frequently Asked Questions
Can alumni still use the library? Graduated alumni may apply for an Alumni Borrower card, which grants Community Borrower-l...

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
  2. [Doc ID: 28] 3. Recalls, Renewals & Holds
3.1 Recalls
Any circulating item may be recalled if another patron requests it, shortening the current borrower's due dat...
  3. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...

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
  2. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...
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
- **Answer Produced:** No....
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] No....
  2. [Doc ID: 25] We are committed to protecting your privacy....
  3. [Doc ID: 23] Postings are limited to 30 days....

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 32] No....
  3. [Doc ID: 25] We are committed to protecting your privacy....

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ❌ No (Expected Doc ID: 4)
- **Answer Produced:** It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....
- **Retrieved Chunks Order:**
  1. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....
  2. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  3. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....

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
  3. [Doc ID: 32] No....

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 6] The novel explores themes of politics, religion, ecology, and human power. Paul must navigate betrayal, lead the indigenous Fremen people, and fulfill...
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851....

**Question 15:** What does the document state regarding: Maple Hill University Library System Graduate & Undergraduate Services Guide 2026-2027 Aca?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01760...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...
  2. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  3. [Doc ID: 29] Interlibrary Loan & Consortium Borrowing
Maple Hill University is a member of the Bay State Academic Consortium, granting students and faculty direct
...

**Question 16:** What does the document state regarding: Library Access & Hours Maple Hill University Library operates two main facilities: the Cal?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 29] Interlibrary Loan & Consortium Borrowing
Maple Hill University is a member of the Bay State Academic Consortium, granting students and faculty direct
...
  3. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...

**Question 17:** What does the document state regarding: Access to both requires a valid MHU ID card, tapped at the turnstile entrance?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...
  3. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...

**Question 18:** What does the document state regarding: student, faculty, or staff request?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** A fee of $25 per hour applies....
- **Retrieved Chunks Order:**
  1. [Doc ID: 22] A fee of $25 per hour applies....
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 28] Borrower Categories & Privileges
Category
Loan Limit
Loan Period
Recall Priority
Undergraduate
30 items
28 days
Standard
Graduate Student
75 items
90 ...

**Question 19:** What does the document state regarding: Faculty loans on course reserve materials are exempt from recall during the semester in wh?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught. 3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  3. [Doc ID: 28] 3. Recalls, Renewals & Holds
3.1 Recalls
Any circulating item may be recalled if another patron requests it, shortening the current borrower's due dat...

**Question 20:** What does the document state regarding: 1 Group Study Rooms Callahan Library offers 14 group study rooms bookable up to 7 days in ?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  3. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...

**Question 21:** What does the document state regarding: The Whitfield Annex offers 4 graduate-only study rooms, bookable up to 14 days in advance,?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 22:** What does the document state regarding: A People's History of the United States Howard Zinn Book / E-book 5 The Structure of Scien?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....
  3. [Doc ID: 30] 7. Collection Highlights
The catalog below reflects a sample of heavily used course-reserve and general-collection titles as of this
guide's printing....

**Question 23:** What does the document state regarding: 4 Life & Physical Sciences Title Author Format Copies Campbell Biology Urry, Cain, Wasserm?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 7. Collection Highlights
The catalog below reflects a sample of heavily used course-reserve and general-collection titles as of this
guide's printing....
  3. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...

**Question 24:** What does the document state regarding: Undergraduate and graduate loan periods automatically extend through the summer term for a?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 31] Frequently Asked Questions
Can alumni still use the library? Graduated alumni may apply for an Alumni Borrower card, which grants Community Borrower-l...
  3. [Doc ID: 28] Borrower Categories & Privileges
Category
Loan Limit
Loan Period
Recall Priority
Undergraduate
30 items
28 days
Standard
Graduate Student
75 items
90 ...

**Question 25:** What does the document state regarding: Can I request a course reserve item be scanned instead of checked out? Instructors can req?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...

### Config 4: Semantic (Hybrid RRF)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  3. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
  2. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  3. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  3. [Doc ID: 21] Free parking is available for all library visitors in the north parking lot. Patrons must display a valid parking permit on their dashboard if parking...

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...
  2. [Doc ID: 28] 3. Recalls, Renewals & Holds
3.1 Recalls
Any circulating item may be recalled if another patron requests it, shortening the current borrower's due dat...
  3. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
  2. [Doc ID: 31] Frequently Asked Questions
Can alumni still use the library? Graduated alumni may apply for an Alumni Borrower card, which grants Community Borrower-l...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
- **Retrieved Chunks Order:**
  1. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 32] No....

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

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
  3. [Doc ID: 24] Emergency exits are clearly marked on all floors. Evacuation routes lead to the south parking lot. Please do not use the elevators during an evacuatio...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851....

**Question 15:** What does the document state regarding: Maple Hill University Library System Graduate & Undergraduate Services Guide 2026-2027 Aca?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01760...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...
  2. [Doc ID: 29] Interlibrary Loan & Consortium Borrowing
Maple Hill University is a member of the Bay State Academic Consortium, granting students and faculty direct
...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 16:** What does the document state regarding: Library Access & Hours Maple Hill University Library operates two main facilities: the Cal?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 29] Interlibrary Loan & Consortium Borrowing
Maple Hill University is a member of the Bay State Academic Consortium, granting students and faculty direct
...
  3. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...

**Question 17:** What does the document state regarding: Access to both requires a valid MHU ID card, tapped at the turnstile entrance?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...
  3. [Doc ID: 15] Phone calls must be taken in the lobby. Headphones must be used for audio devices and kept at a low volume....

**Question 18:** What does the document state regarding: student, faculty, or staff request?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught. 3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 28] Borrower Categories & Privileges
Category
Loan Limit
Loan Period
Recall Priority
Undergraduate
30 items
28 days
Standard
Graduate Student
75 items
90 ...
  3. [Doc ID: 25] The library does not disclose information about borrowed books, search histories, or personal details to third parties unless required by law. Patron ...

**Question 19:** What does the document state regarding: Faculty loans on course reserve materials are exempt from recall during the semester in wh?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught. 3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  3. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...

**Question 20:** What does the document state regarding: 1 Group Study Rooms Callahan Library offers 14 group study rooms bookable up to 7 days in ?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...

**Question 21:** What does the document state regarding: The Whitfield Annex offers 4 graduate-only study rooms, bookable up to 14 days in advance,?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 22:** What does the document state regarding: A People's History of the United States Howard Zinn Book / E-book 5 The Structure of Scien?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 7. Collection Highlights
The catalog below reflects a sample of heavily used course-reserve and general-collection titles as of this
guide's printing....
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 23:** What does the document state regarding: 4 Life & Physical Sciences Title Author Format Copies Campbell Biology Urry, Cain, Wasserm?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 7. Collection Highlights
The catalog below reflects a sample of heavily used course-reserve and general-collection titles as of this
guide's printing....
  3. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...

**Question 24:** What does the document state regarding: Undergraduate and graduate loan periods automatically extend through the summer term for a?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 28] Borrower Categories & Privileges
Category
Loan Limit
Loan Period
Recall Priority
Undergraduate
30 items
28 days
Standard
Graduate Student
75 items
90 ...
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 25:** What does the document state regarding: Can I request a course reserve item be scanned instead of checked out? Instructors can req?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

### Config 5: Semantic (Hybrid + Reranker)

**Question 1:** Is the library open on New Year's Day?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 1] Holiday schedules vary: we are closed on Christmas Day, New Year's Day, and Thanksgiving Day. On other national holidays, we usually close at 2:00 PM....
  3. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....

**Question 2:** Are the library hours different during finals?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 1] The library is closed on Sundays to allow for deep cleaning and staff rest. During exam weeks, hours are extended until midnight....
  3. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...

**Question 3:** What time can I visit on a weekday morning?

- **Hit:** ✅ Yes (Expected Doc ID: 1)
- **Answer Produced:** The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the evening to accommodate students and local residents. O...
- **Retrieved Chunks Order:**
  1. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  2. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  3. [Doc ID: 21] Free parking is available for all library visitors in the north parking lot. Patrons must display a valid parking permit on their dashboard if parking...

**Question 4:** Can I renew a book more than one time?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

**Question 5:** Can I take a magazine or reference book home with me?

- **Hit:** ✅ Yes (Expected Doc ID: 2)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 2] Reference books, current issues of periodicals, and rare manuscripts cannot be checked out and must be read within the library reading room....
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

**Question 6:** How much extra time do I get after the due date before I'm charged?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $15 max
$1.00/hour
$5.00/day
Faculty
No fine, recall...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...
  2. [Doc ID: 28] 3. Recalls, Renewals & Holds
3.1 Recalls
Any circulating item may be recalled if another patron requests it, shortening the current borrower's due dat...
  3. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....

**Question 7:** What happens if I destroy a book I borrowed?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
- **Retrieved Chunks Order:**
  1. [Doc ID: 3] If a book is lost or damaged beyond repair, the member must pay the replacement cost of the book plus a processing fee of $10.00....
  2. [Doc ID: 31] Frequently Asked Questions
Can alumni still use the library? Graduated alumni may apply for an Alumni Borrower card, which grants Community Borrower-l...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 8:** Where can I drop off books after closing time?

- **Hit:** ✅ Yes (Expected Doc ID: 3)
- **Answer Produced:** We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
- **Retrieved Chunks Order:**
  1. [Doc ID: 11] We welcome donations of gently used books, CDs, and DVDs. Donations can be dropped off at the designated bin near the side entrance....
  2. [Doc ID: 1] The library operates on a structured weekly schedule. From Monday to Friday, the doors open at 9:00 AM in the morning and close at 8:00 PM in the even...
  3. [Doc ID: 3] All borrowed books must be returned within the designated 14-day loan period to avoid penalties. Return points include the main reception desk inside ...

**Question 9:** Can someone without a fixed home address still sign up?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 32] No....

**Question 10:** Do university students need to fill out a separate application?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
- **Retrieved Chunks Order:**
  1. [Doc ID: 12] High school students can earn community service hours. Interested individuals must fill out an application and pass a background check....
  2. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...
  3. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...

**Question 11:** How many electronic books can I access with my membership?

- **Hit:** ✅ Yes (Expected Doc ID: 4)
- **Answer Produced:** Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan period is 14 calendar days (two weeks) from the check...
- **Retrieved Chunks Order:**
  1. [Doc ID: 2] Members of our library enjoy generous borrowing privileges. Standard members can borrow up to 3 physical books at any given time. The default loan per...
  2. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...
  3. [Doc ID: 4] Library membership is free of charge for all local residents and students. To register, visit the front desk and present a valid government-issued pho...

**Question 12:** What object does Bilbo find on his journey that becomes important later?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  2. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  3. [Doc ID: 17] It details the voyage of the whaling ship Pequod, commanded by Captain Ahab. Ahab is obsessed with seeking revenge on Moby Dick, a giant white sperm w...

**Question 13:** Which mountain do the dwarves want to reclaim from the dragon?

- **Hit:** ✅ Yes (Expected Doc ID: 5)
- **Answer Produced:** The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical world of Middle-earth. The story follows the quest of...
- **Retrieved Chunks Order:**
  1. [Doc ID: 5] The Hobbit is a masterpiece of classic fantasy literature written by J.R.R. Tolkien and published in 1937. It introduces the reader to the magical wor...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 24] Emergency exits are clearly marked on all floors. Evacuation routes lead to the south parking lot. Please do not use the elevators during an evacuatio...

**Question 14:** What natural resource makes space travel possible in Dune, and where is it found?

- **Hit:** ✅ Yes (Expected Doc ID: 6)
- **Answer Produced:** Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tells the story of young Paul Atreides as his family ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 6] Dune is a landmark science fiction novel written by Frank Herbert and published in 1965. Set in a far-distant future in an interstellar empire, it tel...
  2. [Doc ID: 5] Along the way, Bilbo finds a mysterious magic ring that makes him invisible, which plays a major role in Tolkien's sequel, The Lord of the Rings....
  3. [Doc ID: 17] Moby-Dick is an epic novel written by Herman Melville and published in 1851....

**Question 15:** What does the document state regarding: Maple Hill University Library System Graduate & Undergraduate Services Guide 2026-2027 Aca?

- **Hit:** ✅ Yes (Expected Doc ID: 27)
- **Answer Produced:** Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01760...
- **Retrieved Chunks Order:**
  1. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...
  2. [Doc ID: 29] Interlibrary Loan & Consortium Borrowing
Maple Hill University is a member of the Bay State Academic Consortium, granting students and faculty direct
...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 16:** What does the document state regarding: Library Access & Hours Maple Hill University Library operates two main facilities: the Cal?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 29] Interlibrary Loan & Consortium Borrowing
Maple Hill University is a member of the Bay State Academic Consortium, granting students and faculty direct
...
  3. [Doc ID: 27] Maple Hill University Library System
Graduate & Undergraduate Services Guide
2026-2027 Academic Year Edition
410 University Parkway, Maple Hill, MA 01...

**Question 17:** What does the document state regarding: Access to both requires a valid MHU ID card, tapped at the turnstile entrance?

- **Hit:** ✅ Yes (Expected Doc ID: 28)
- **Answer Produced:** 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, and the Whitfield Research Annex for graduate, fac...
- **Retrieved Chunks Order:**
  1. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...
  2. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...
  3. [Doc ID: 15] Phone calls must be taken in the lobby. Headphones must be used for audio devices and kept at a low volume....

**Question 18:** What does the document state regarding: student, faculty, or staff request?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught. 3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 28] Borrower Categories & Privileges
Category
Loan Limit
Loan Period
Recall Priority
Undergraduate
30 items
28 days
Standard
Graduate Student
75 items
90 ...
  3. [Doc ID: 25] The library does not disclose information about borrowed books, search histories, or personal details to third parties unless required by law. Patron ...

**Question 19:** What does the document state regarding: Faculty loans on course reserve materials are exempt from recall during the semester in wh?

- **Hit:** ✅ Yes (Expected Doc ID: 29)
- **Answer Produced:** student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught. 3.2 Renewals
Items may be renewed up to 6 times ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  2. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  3. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...

**Question 20:** What does the document state regarding: 1 Group Study Rooms Callahan Library offers 14 group study rooms bookable up to 7 days in ?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 32] Group study rooms are reserved for current students, faculty, and staff. Community borrowers may use
general seating areas but cannot book private roo...

**Question 21:** What does the document state regarding: The Whitfield Annex offers 4 graduate-only study rooms, bookable up to 14 days in advance,?

- **Hit:** ✅ Yes (Expected Doc ID: 30)
- **Answer Produced:** 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no other booking follows. The Whitfield Annex offers 4 ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 30] 6.1 Group Study Rooms
Callahan Library offers 14 group study rooms bookable up to 7 days in advance for sessions of up to 3 hours,
extendable if no ot...
  2. [Doc ID: 9] Quiet study rooms are available for individual or group study. Rooms can be booked for up to 2 hours per day. Bookings must be made in advance online ...
  3. [Doc ID: 28] 1. Library Access & Hours
Maple Hill University Library operates two main facilities: the Callahan Library for undergraduate and general
collections, ...

**Question 22:** What does the document state regarding: A People's History of the United States Howard Zinn Book / E-book 5 The Structure of Scien?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 7. Collection Highlights
The catalog below reflects a sample of heavily used course-reserve and general-collection titles as of this
guide's printing....
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 23:** What does the document state regarding: 4 Life & Physical Sciences Title Author Format Copies Campbell Biology Urry, Cain, Wasserm?

- **Hit:** ✅ Yes (Expected Doc ID: 31)
- **Answer Produced:** A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said
Book
2
Guns, Germs, and Steel
Jared Diamond
Book ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 31] A People's History of the United States
Howard Zinn
Book / E-book
5
The Structure of Scientific Revolutions
Thomas Kuhn
Book
3
Orientalism
Edward Said...
  2. [Doc ID: 30] 7. Collection Highlights
The catalog below reflects a sample of heavily used course-reserve and general-collection titles as of this
guide's printing....
  3. [Doc ID: 29] Fines & Billing
Category
Standard Items
Course Reserves
Equipment
Undergraduate
$0.25/day, $15 max
$1.00/hour
$5.00/day
Graduate Student
$0.25/day, $1...

**Question 24:** What does the document state regarding: Undergraduate and graduate loan periods automatically extend through the summer term for a?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 28] Borrower Categories & Privileges
Category
Loan Limit
Loan Period
Recall Priority
Undergraduate
30 items
28 days
Standard
Graduate Student
75 items
90 ...
  3. [Doc ID: 10] It typically takes 5 to 7 business days for a book to arrive. Loan periods are set by the lending library....

**Question 25:** What does the document state regarding: Can I request a course reserve item be scanned instead of checked out? Instructors can req?

- **Hit:** ✅ Yes (Expected Doc ID: 32)
- **Answer Produced:** Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring semester, provided the borrower remains enrolled ...
- **Retrieved Chunks Order:**
  1. [Doc ID: 32] Undergraduate and graduate loan periods automatically extend through the summer term for any items
checked out during the last two weeks of the spring...
  2. [Doc ID: 29] student, faculty, or staff request. Faculty loans on course reserve materials are exempt from recall during the
semester in which the course is taught...
  3. [Doc ID: 10] If our library does not have a book you need, you can request it through interlibrary loan. We partner with other libraries across the region to share...

