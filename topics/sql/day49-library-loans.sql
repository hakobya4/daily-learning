-- Day 49, Task 6 -- SQL: anti-join, HAVING, window LAG on dates, conditional aggregation.
--
-- Self-contained. Load with: sqlite3 practice_day49.db < day49-library-loans.sql
--
-- THE PROBLEM
-- members(id, name), loans(id, member_id, book, loaned, returned). returned is NULL while
-- the book is still out. Dates are ISO text. Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Members who have NEVER borrowed anything. Output: name. Order by name.
-- Q2: Per member, number of loans and number still out. Output: name, total, still_out
--     (members with no loans omitted). Order by total DESC, name.
-- Q3: Members with 2 or more loans of the SAME book. Output: name, book, n. Order by name, book.
-- Q4: For each member, days since their previous loan began, for every loan that has a
--     previous one. Output: name, book, gap_days. Order by name, loaned.
--     Hint: LAG(loaned) OVER (PARTITION BY member_id ORDER BY loaned), julianday().
--
-- Expected results for the data below:
--   Q1: dara
--   Q2: ana|4|1  ben|2|1  cy|1|0
--   Q3: ana|Dune|2
--   Q4: ana|Emma|10  ana|Dune|15  ana|Ulysses|15  ben|Hamlet|20

CREATE TABLE members (id INTEGER, name TEXT);
INSERT INTO members VALUES (1,'ana'),(2,'ben'),(3,'cy'),(4,'dara');
CREATE TABLE loans (id INTEGER, member_id INTEGER, book TEXT, loaned TEXT, returned TEXT);
INSERT INTO loans VALUES
 (1,1,'Dune','2026-03-01','2026-03-10'),
 (2,1,'Emma','2026-03-11','2026-03-20'),
 (3,1,'Dune','2026-03-26','2026-04-02'),
 (4,1,'Ulysses','2026-04-10',NULL),
 (5,2,'Emma','2026-03-05','2026-03-15'),
 (6,2,'Hamlet','2026-03-25',NULL),
 (7,3,'Dune','2026-03-07','2026-03-09');

-- Q1

-- Q2

-- Q3

-- Q4
