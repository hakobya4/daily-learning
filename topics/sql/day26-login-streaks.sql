-- Day 26, Task 1 -- SQL: gaps and islands (consecutive-day login streaks).
--
-- Self-contained. Load with: sqlite3 practice_day26.db < day26-login-streaks.sql
--
-- THE PROBLEM
-- logins has one row per (user_id, day) = the user logged in that day.
-- Write 3 queries. Nothing pre-solved.
--
-- Q1: Users who have a streak of at least 3 consecutive days:
--     user_id only, one row per user, ordered by user_id.
-- Q2: The longest streak per user: user_id, streak_len, start_day, end_day.
--     On a tie take the earlier streak. Order by user_id.
-- Q3: For every day: day, active_users, new_users (users whose FIRST login
--     ever is that day). Order by day.
--
-- HINT: the classic trick -- day minus ROW_NUMBER() (as a number of days)
-- is constant inside one run of consecutive days, e.g.
--   date(day, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) || ' days')
-- Group by user_id and that value to get each island.

DROP TABLE IF EXISTS logins;
CREATE TABLE logins (
    user_id INTEGER NOT NULL,
    day     TEXT NOT NULL,
    PRIMARY KEY (user_id, day)
);
INSERT INTO logins (user_id, day) VALUES
    (1, '2026-03-01'), (1, '2026-03-02'), (1, '2026-03-03'), (1, '2026-03-05'), (1, '2026-03-06'),
    (2, '2026-03-01'), (2, '2026-03-03'), (2, '2026-03-05'),
    (3, '2026-03-02'), (3, '2026-03-03'), (3, '2026-03-04'), (3, '2026-03-05'), (3, '2026-03-09'),
    (4, '2026-03-06'), (4, '2026-03-07');

-- Q1: TODO write the query
-- Q2: TODO write the query
-- Q3: TODO write the query
