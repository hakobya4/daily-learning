-- Day 22, Task 1 -- SQL: sessionization (split events into sessions on a gap).
--
-- Self-contained. Load with: sqlite3 practice_day22.db < day22-sessionization.sql
--
-- THE PROBLEM
-- clicks_sql has one row per click (user, timestamp in 'YYYY-MM-DD HH:MM:SS').
-- A new SESSION starts when the gap since the user's previous click is
-- MORE than 30 minutes (exactly 30 minutes stays in the same session),
-- or when it is the user's first click. Write 3 queries. Nothing pre-solved.
--
-- Q1: Label every click with a per-user session number (1, 2, ...):
--     user_name, ts, session_no. Order by user_name, ts.
-- Q2: One row per session: user_name, session_no, session_start,
--     session_end, clicks, minutes (end - start, whole minutes).
--     Order by user_name, session_no.
-- Q3: The user with the most sessions overall: user_name, sessions.
--     (There is no tie in this data.)
--
-- HINT: LAG(ts) OVER (PARTITION BY user_name ORDER BY ts) gives the previous
-- click; flag rows where the gap > 30 min (use strftime('%s', ts) for
-- seconds) as 1 else 0, then SUM(flag) OVER (...) is the session number.

DROP TABLE IF EXISTS clicks_sql;
CREATE TABLE clicks_sql (
    user_name TEXT NOT NULL,
    ts        TEXT NOT NULL,
    PRIMARY KEY (user_name, ts)
);
INSERT INTO clicks_sql (user_name, ts) VALUES
    ('ana', '2026-10-01 09:00:00'), ('ana', '2026-10-01 09:10:00'),
    ('ana', '2026-10-01 09:40:00'), ('ana', '2026-10-01 11:00:00'),
    ('ana', '2026-10-01 11:05:00'),
    ('ben', '2026-10-01 10:00:00'), ('ben', '2026-10-01 10:31:00'),
    ('ben', '2026-10-01 15:00:00'), ('ben', '2026-10-02 09:00:00'),
    ('ben', '2026-10-02 09:20:00'),
    ('cy',  '2026-10-01 08:00:00'), ('cy',  '2026-10-01 08:30:00'),
    ('cy',  '2026-10-01 09:00:00');

-- Q1:

-- Q2:

-- Q3:
