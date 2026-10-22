-- Day 32, Task 1 -- SQL: gaps and islands (consecutive login streaks).
--
-- Self-contained. Load with: sqlite3 practice_day32.db < day32-login-streaks.sql
--
-- THE PROBLEM
-- logins(user, day) holds one row per user per calendar day they logged in
-- (days are ISO dates, no duplicates). Write 3 queries. Nothing pre-solved.
--
-- Q1: Every streak (maximal run of consecutive calendar days) per user.
--     Output: user, start_day, end_day, length. Order by user, start_day.
-- Q2: The longest streak per user (no ties in this data).
--     Output: user, length. Order by user.
-- Q3: Users who have at least one streak of 3 or more days.
--     Output: user. Order by user.
--
-- HINT: classic "gaps and islands": ROW_NUMBER() OVER (PARTITION BY user
-- ORDER BY day) subtracted from the day (julianday(day) - rn) is constant
-- inside a streak, so GROUP BY user and that value.
--
-- Expected results for the data below:
--   Q1: ann 2026-01-01 2026-01-03 3 / ann 2026-01-05 2026-01-05 1 /
--       bob 2026-01-02 2026-01-03 2 / bob 2026-01-07 2026-01-10 4 /
--       cy  2026-01-04 2026-01-04 1
--   Q2: ann 3 / bob 4 / cy 1
--   Q3: ann / bob

DROP TABLE IF EXISTS logins;
CREATE TABLE logins ("user" TEXT NOT NULL, day TEXT NOT NULL);
INSERT INTO logins ("user", day) VALUES
    ('ann','2026-01-01'),('ann','2026-01-02'),('ann','2026-01-03'),('ann','2026-01-05'),
    ('bob','2026-01-02'),('bob','2026-01-03'),
    ('bob','2026-01-07'),('bob','2026-01-08'),('bob','2026-01-09'),('bob','2026-01-10'),
    ('cy','2026-01-04');

-- Q1
-- TODO

-- Q2
-- TODO

-- Q3
-- TODO
