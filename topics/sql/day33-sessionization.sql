-- Day 33, Task 1 -- SQL: sessionization (new session after a 30-minute gap).
--
-- Self-contained. Load with: sqlite3 practice_day33.db < day33-sessionization.sql
--
-- THE PROBLEM
-- events(user, ts) holds one row per click; ts is 'YYYY-MM-DD HH:MM:SS'
-- (no duplicates per user). A user's session ends when the next event is
-- MORE than 30 minutes after the previous one (exactly 30 minutes still
-- continues the session). Write 3 queries. Nothing pre-solved.
--
-- Q1: Every session per user, numbered 1,2,... in time order.
--     Output: user, session_no, start_ts, end_ts, event_count.
--     Order by user, session_no.
-- Q2: The longest session per user by duration in minutes (end - start;
--     no ties in this data). Output: user, minutes. Order by user.
-- Q3: Total number of sessions across all users, as a single column
--     named sessions.
--
-- HINT: LAG(ts) OVER (PARTITION BY user ORDER BY ts) gives the previous
-- event; flag a row 1 when there is no previous event or the gap
-- (julianday difference * 1440) is > 30; a running SUM() of the flag is
-- the session number; then GROUP BY user, session_no.
--
-- Expected results for the data below:
--   Q1: ann 1 2026-02-01 09:00:00 2026-02-01 09:10:00 2 / ann 2
--       2026-02-01 09:40:00 2026-02-01 09:40:00 1 / ann 3 2026-02-01
--       10:11:00 2026-02-01 10:20:00 2 / ann 4 2026-02-02 08:00:00
--       2026-02-02 08:00:00 1 / bob 1 2026-02-01 23:50:00 2026-02-02
--       00:15:00 2 / bob 2 2026-02-02 00:46:00 2026-02-02 00:50:00 2 /
--       bob 3 2026-02-02 13:00:00 2026-02-02 13:00:00 1 / cy 1 2026-02-03
--       12:00:00 2026-02-03 12:00:00 1
--   Q2: ann 10 / bob 25 / cy 0
--   Q3: 8

DROP TABLE IF EXISTS events;
CREATE TABLE events ("user" TEXT NOT NULL, ts TEXT NOT NULL);
INSERT INTO events ("user", ts) VALUES
    ('ann','2026-02-01 09:00:00'),('ann','2026-02-01 09:10:00'),('ann','2026-02-01 09:40:00'),
    ('ann','2026-02-01 10:11:00'),('ann','2026-02-01 10:20:00'),('ann','2026-02-02 08:00:00'),
    ('bob','2026-02-01 23:50:00'),('bob','2026-02-02 00:15:00'),('bob','2026-02-02 00:46:00'),
    ('bob','2026-02-02 00:50:00'),('bob','2026-02-02 13:00:00'),
    ('cy','2026-02-03 12:00:00');

-- Q1 --
WITH flagged AS (
    SELECT "user", ts,
           CASE WHEN LAG(ts) OVER (PARTITION BY "user" ORDER BY ts) IS NULL
                  OR (julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY "user" ORDER BY ts))) * 1440 > 30
                THEN 1 ELSE 0 END AS new_session
    FROM events
), numbered AS (
    SELECT "user", ts,
           SUM(new_session) OVER (PARTITION BY "user" ORDER BY ts) AS session_no
    FROM flagged
)
SELECT "user", session_no, MIN(ts) AS start_ts, MAX(ts) AS end_ts, COUNT(*) AS event_count
FROM numbered
GROUP BY "user", session_no
ORDER BY "user", session_no;

-- Q2 --
WITH flagged AS (
    SELECT "user", ts,
           CASE WHEN LAG(ts) OVER (PARTITION BY "user" ORDER BY ts) IS NULL
                  OR (julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY "user" ORDER BY ts))) * 1440 > 30
                THEN 1 ELSE 0 END AS new_session
    FROM events
), numbered AS (
    SELECT "user", ts,
           SUM(new_session) OVER (PARTITION BY "user" ORDER BY ts) AS session_no
    FROM flagged
), sessions AS (
    SELECT "user", session_no,
           CAST(ROUND((julianday(MAX(ts)) - julianday(MIN(ts))) * 1440) AS INTEGER) AS minutes
    FROM numbered
    GROUP BY "user", session_no
)
SELECT "user", MAX(minutes) AS minutes
FROM sessions
GROUP BY "user"
ORDER BY "user";

-- Q3 --
WITH flagged AS (
    SELECT CASE WHEN LAG(ts) OVER (PARTITION BY "user" ORDER BY ts) IS NULL
                  OR (julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY "user" ORDER BY ts))) * 1440 > 30
                THEN 1 ELSE 0 END AS new_session
    FROM events
)
SELECT SUM(new_session) AS sessions FROM flagged;
