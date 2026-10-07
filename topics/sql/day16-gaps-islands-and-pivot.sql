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
SELECT user, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS length
FROM (
    SELECT user, day, day - ROW_NUMBER() OVER (PARTITION BY user ORDER BY day) AS grp
    FROM logins
)
GROUP BY user, grp
ORDER BY user, start_day;


-- Q2
SELECT user, MAX(length) AS longest
FROM (
    SELECT user, COUNT(*) AS length
    FROM (
        SELECT user, day, day - ROW_NUMBER() OVER (PARTITION BY user ORDER BY day) AS grp
        FROM logins
    )
    GROUP BY user, grp
)
GROUP BY user
ORDER BY longest DESC, user;


-- Q3
SELECT user, day + 1 AS gap_start, next_day - 1 AS gap_end
FROM (
    SELECT user, day, LEAD(day) OVER (PARTITION BY user ORDER BY day) AS next_day
    FROM logins
)
WHERE next_day IS NOT NULL AND next_day - day > 1
ORDER BY user, gap_start;


-- Q4
SELECT u.user,
       COALESCE(SUM(CASE WHEN o.status = 'paid' THEN o.amount END), 0) AS paid,
       COALESCE(SUM(CASE WHEN o.status = 'refunded' THEN o.amount END), 0) AS refunded,
       COALESCE(SUM(CASE WHEN o.status = 'pending' THEN o.amount END), 0) AS pending
FROM (SELECT DISTINCT user FROM logins UNION SELECT DISTINCT user FROM orders) AS u
LEFT JOIN orders o ON o.user = u.user
GROUP BY u.user
ORDER BY u.user;


-- Q5
SELECT l.user
FROM logins l
GROUP BY l.user
HAVING COUNT(DISTINCT l.day) >= 3
   AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.user = l.user AND o.status = 'paid')
ORDER BY l.user;

