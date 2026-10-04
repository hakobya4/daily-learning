-- Day 13, Task 1 -- SQL: dedupe with ROW_NUMBER, latest-per-group, pivot, anti-join.
--
-- Self-contained. Load with: sqlite3 practice_day13.db < day13-dedupe-and-pivot.sql
--
-- THE PROBLEM
-- events(id, user_id, kind, ts) where ts is 'YYYY-MM-DD HH:MM'.
-- Write 4 queries. Nothing is pre-solved.
--
-- Q1: Latest event per user (user_id, kind, ts). Use ROW_NUMBER() OVER
--     (PARTITION BY user_id ORDER BY ts DESC, id DESC). Order by user_id.
-- Q2: Remove duplicates: rows with the same (user_id, kind, ts) are
--     duplicates. Return the ids of the rows to DELETE (keep the lowest
--     id of each group). Order by id.
-- Q3: Pivot: one row per user with counts per kind as columns
--     (user_id, logins, views, purchases) using SUM(CASE WHEN ...).
--     Order by user_id.
-- Q4: Users who viewed something but NEVER purchased (user_id).
--     Use NOT EXISTS (or LEFT JOIN ... IS NULL). Order by user_id.

DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    kind    TEXT NOT NULL,   -- 'login' | 'view' | 'purchase'
    ts      TEXT NOT NULL
);
INSERT INTO events (id, user_id, kind, ts) VALUES
    (1,  1, 'login',    '2026-03-01 09:00'),
    (2,  1, 'view',     '2026-03-01 09:05'),
    (3,  1, 'view',     '2026-03-01 09:05'),
    (4,  1, 'purchase', '2026-03-01 09:30'),
    (5,  2, 'login',    '2026-03-02 10:00'),
    (6,  2, 'view',     '2026-03-02 10:02'),
    (7,  2, 'view',     '2026-03-02 10:10'),
    (8,  3, 'login',    '2026-03-02 11:00'),
    (9,  3, 'login',    '2026-03-02 11:00'),
    (10, 3, 'purchase', '2026-03-03 08:15'),
    (11, 4, 'view',     '2026-03-03 12:00'),
    (12, 4, 'login',    '2026-03-04 07:45');

-- Q1
SELECT user_id, kind, ts
FROM (
    SELECT user_id, kind, ts,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts DESC, id DESC) AS rn
    FROM events
)
WHERE rn = 1
ORDER BY user_id;

-- Q2
SELECT id
FROM (
    SELECT id,
           ROW_NUMBER() OVER (PARTITION BY user_id, kind, ts ORDER BY id) AS rn
    FROM events
)
WHERE rn > 1
ORDER BY id;

-- Q3
SELECT user_id,
       SUM(CASE WHEN kind = 'login'    THEN 1 ELSE 0 END) AS logins,
       SUM(CASE WHEN kind = 'view'     THEN 1 ELSE 0 END) AS views,
       SUM(CASE WHEN kind = 'purchase' THEN 1 ELSE 0 END) AS purchases
FROM events
GROUP BY user_id
ORDER BY user_id;

-- Q4
SELECT DISTINCT e.user_id
FROM events e
WHERE e.kind = 'view'
  AND NOT EXISTS (
      SELECT 1 FROM events p
      WHERE p.user_id = e.user_id AND p.kind = 'purchase'
  )
ORDER BY e.user_id;
