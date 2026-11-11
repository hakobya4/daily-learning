-- Day 52, Task 6 -- SQL: sessionization with LAG (gaps and islands on timestamps).
--
-- Self-contained. Load with: sqlite3 practice_day52.db < day52-sessions-gaps.sql
--
-- THE PROBLEM
-- page_views(user_id, ts, page) -- ts is 'YYYY-MM-DD HH:MM'. A SESSION is a maximal run of a
-- user's views where each view is at most 30 minutes after the previous one; a gap of MORE
-- than 30 minutes starts a new session. Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: For every view, the minutes since the same user's previous view (NULL for their first).
--     Output: user_id, ts, gap_min. Order by user_id, ts.
--     Hint: LAG(ts) OVER (PARTITION BY user_id ORDER BY ts); minutes in SQLite =
--     ROUND((julianday(a) - julianday(b)) * 1440), cast to INTEGER.
-- Q2: Number of sessions per user. Output: user_id, sessions. Order by user_id.
--     Hint: flag 1 where gap IS NULL OR gap > 30, then a running SUM of the flag = session id.
-- Q3: One row per session: user_id, session_start, views, duration_min (last view minus first
--     view; a single-view session lasts 0). Order by user_id, session_start.
-- Q4: Each user's longest session duration. Output: user_id, longest_min.
--     Order by longest_min DESC, user_id.
--
-- Expected results for the data below:
--   Q1: ann|09:00|NULL  ann|09:10|10  ann|09:35|25  ann|11:00|85  ann|11:20|20
--       bob|10:00|NULL  bob|10:31|31  bob|10:45|14
--       cat|08:00|NULL  cat|08:05|5   cat|08:30|25  cat|08:55|25   dan|12:00|NULL
--       (ts shown abbreviated; output the full '2026-05-01 HH:MM' value)
--   Q2: ann|2  bob|2  cat|1  dan|1
--   Q3: ann|2026-05-01 09:00|3|35  ann|2026-05-01 11:00|2|20
--       bob|2026-05-01 10:00|1|0   bob|2026-05-01 10:31|2|14
--       cat|2026-05-01 08:00|4|55  dan|2026-05-01 12:00|1|0
--   Q4: cat|55  ann|35  bob|14  dan|0

CREATE TABLE page_views (user_id TEXT, ts TEXT, page TEXT);
INSERT INTO page_views VALUES
 ('ann','2026-05-01 09:00','home'),
 ('ann','2026-05-01 09:10','cart'),
 ('ann','2026-05-01 09:35','pay'),
 ('ann','2026-05-01 11:00','home'),
 ('ann','2026-05-01 11:20','help'),
 ('bob','2026-05-01 10:00','home'),
 ('bob','2026-05-01 10:31','home'),
 ('bob','2026-05-01 10:45','cart'),
 ('cat','2026-05-01 08:00','home'),
 ('cat','2026-05-01 08:05','help'),
 ('cat','2026-05-01 08:30','help'),
 ('cat','2026-05-01 08:55','pay'),
 ('dan','2026-05-01 12:00','home');

-- Q1
-- TODO: your query here

-- Q2
-- TODO: your query here

-- Q3
-- TODO: your query here

-- Q4
-- TODO: your query here
