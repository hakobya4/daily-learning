-- Day 21, Task 1 -- SQL: gaps and islands (consecutive-day streaks).
--
-- Self-contained. Load with: sqlite3 practice_day21.db < day21-gaps-and-islands.sql
--
-- THE PROBLEM
-- logins_sql has one row per user per day they logged in (ISO dates).
-- Write 3 queries. Nothing pre-solved.
--
-- Q1: For each user, the longest streak of consecutive login days
--     (columns: user_name, longest_streak). Order by user_name.
-- Q2: List every streak ("island") of every user: user_name,
--     streak_start, streak_end, streak_days. Order by user_name,
--     streak_start.
-- Q3: Users whose logins form exactly ONE streak (no gaps at all):
--     user_name only. Order by user_name.
--
-- HINT: date(day) minus ROW_NUMBER() OVER (PARTITION BY user_name
-- ORDER BY day) days is constant within a streak -- group by that.
-- In SQLite: date(day, '-' || rn || ' days').

DROP TABLE IF EXISTS logins_sql;
CREATE TABLE logins_sql (
    user_name TEXT NOT NULL,
    day       TEXT NOT NULL,
    PRIMARY KEY (user_name, day)
);
INSERT INTO logins_sql (user_name, day) VALUES
    ('ana',  '2026-09-01'), ('ana',  '2026-09-02'), ('ana',  '2026-09-03'),
    ('ana',  '2026-09-06'), ('ana',  '2026-09-07'),
    ('ben',  '2026-09-10'), ('ben',  '2026-09-11'), ('ben',  '2026-09-12'),
    ('ben',  '2026-09-13'),
    ('cy',   '2026-09-01'), ('cy',   '2026-09-03'), ('cy',   '2026-09-05'),
    ('dee',  '2026-08-30'), ('dee',  '2026-08-31'), ('dee',  '2026-09-01'),
    ('dee',  '2026-09-02'), ('dee',  '2026-09-05'), ('dee',  '2026-09-06'),
    ('dee',  '2026-09-07'), ('dee',  '2026-09-08'), ('dee',  '2026-09-09');

-- Q1:

-- Q2:

-- Q3:
