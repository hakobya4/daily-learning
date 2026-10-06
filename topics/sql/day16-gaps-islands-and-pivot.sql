-- Day 16, Task 1 -- SQL: gaps and islands, conditional pivot, anti-join, self-referencing dedupe.
--
-- Self-contained. Load with: sqlite3 practice_day16.db < day16-gaps-islands-and-pivot.sql
--
-- THE PROBLEM
-- logins(id, user, day) -- one row per user per login day (day is an
-- integer day number); orders(id, user, amount, status). Write 5 queries.
-- Nothing is pre-solved.
--
-- Q1: Islands: for each user, each streak of consecutive login days as
--     (user, start_day, end_day, length). Hint: day - ROW_NUMBER() OVER
--     (PARTITION BY user ORDER BY day) is constant within a streak.
--     Order by user, start_day.
-- Q2: The longest streak per user: (user, longest). Order by longest
--     DESC, user.
-- Q3: Gaps: for each user the missing day ranges between logins, as
--     (user, gap_start, gap_end), using LEAD(day). Order by user,
--     gap_start.
-- Q4: Conditional pivot: one row per user with columns paid, refunded,
--     pending = SUM(amount) per status (0 when none, use COALESCE or
--     SUM(CASE ...)). Include users with no orders. Order by user.
-- Q5: Users who logged in on at least 3 distinct days but never placed
--     an order with status 'paid' (anti-join with NOT EXISTS):
--     (user). Order by user.

DROP TABLE IF EXISTS logins;
DROP TABLE IF EXISTS orders;
CREATE TABLE logins (id INTEGER PRIMARY KEY, user TEXT NOT NULL, day INTEGER NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, user TEXT NOT NULL, amount INTEGER NOT NULL, status TEXT NOT NULL);

INSERT INTO logins (user, day) VALUES
    ('ann', 1), ('ann', 2), ('ann', 3), ('ann', 6), ('ann', 7),
    ('bob', 2), ('bob', 4), ('bob', 5), ('bob', 6), ('bob', 7),
    ('cy', 1), ('cy', 9), ('cy', 10),
    ('di', 3);

INSERT INTO orders (user, amount, status) VALUES
    ('ann', 50, 'paid'), ('ann', 20, 'refunded'), ('ann', 15, 'paid'),
    ('bob', 40, 'pending'),
    ('cy', 10, 'paid'),
    ('di', 5, 'refunded');

-- Q1


-- Q2


-- Q3


-- Q4


-- Q5

