-- Day 63, Task 3 -- SQL: medians, modes and percentiles per group with window functions
-- (no MEDIAN() / PERCENTILE_CONT() -- SQLite has neither).
--
-- Self-contained. Load with: sqlite3 practice_day63.db < day63-median-mode-percentile.sql
-- (SQLite >= 3.25 for window functions.)
-- No sqlite3 CLI? python3 -c "import sqlite3; c=sqlite3.connect(':memory:');
--   c.executescript(open('day63-median-mode-percentile.sql').read())" and run your
--   queries with c.execute(...) just as well.
--
-- THE PROBLEM
-- deliveries(delivery_id, courier, minutes): how long each delivery took.
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Median delivery time per courier: courier, n (number of deliveries), median_minutes.
--     Ordered by courier. For an odd n the median is the middle value; for an even n it
--     is the AVERAGE of the two middle values (so it can be fractional).
--     Hint: ROW_NUMBER() OVER (PARTITION BY courier ORDER BY minutes) AS rn and
--     COUNT(*) OVER (PARTITION BY courier) AS n in a CTE, then keep the rows where
--     rn IN ((n + 1) / 2, (n + 2) / 2) -- with integer division that is one row for
--     odd n and two rows for even n -- and AVG() them per courier.
--     (Check yourself: why does that pair of expressions work for both parities?)
-- Q2: Mode(s) per courier: courier, minutes, times -- every minutes value that occurs
--     most often for that courier, INCLUDING ties (ben has two modes), but only when
--     that maximum frequency is greater than 1 (a courier whose values are all
--     distinct has no mode and does not appear). Ordered by courier, minutes.
--     Hint: GROUP BY courier, minutes to get frequencies, then compare against the
--     per-courier MAX(frequency) -- either a second CTE + JOIN, or
--     MAX(cnt) OVER (PARTITION BY courier), or RANK() OVER (... ORDER BY cnt DESC).
-- Q3: 90th percentile by the NEAREST-RANK method: courier, p90_minutes, slower_than_p90
--     where p90 is the value at rank ceil(0.9 * n) in ascending order (1-based), and
--     slower_than_p90 is how many of that courier's deliveries took STRICTLY longer.
--     Ordered by courier. SQLite before 3.44 has no CEIL(), so compute ceil(9n/10) with
--     integer arithmetic: (9 * n + 9) / 10. (Convince yourself it equals ceil for every
--     n >= 1, and note how small groups make p90 = the maximum.)
--
-- Expected results for the data below:
--   Q1: ana|6|24.5
--       ben|7|30.0
--       chloe|1|25.0
--       dev|10|33.0
--       eli|2|15.0
--   Q2: ana|22|2
--       ben|12|2
--       ben|30|2
--       dev|10|2
--       dev|33|2
--   Q3: ana|41|0
--       ben|60|0
--       chloe|25|0
--       dev|47|1
--       eli|16|0
-- (The sqlite3 CLI prints 30.0 / 25.0 / 33.0 / 15.0 for AVG results; if your client
--  prints 30 instead of 30.0 that is fine.)

DROP TABLE IF EXISTS deliveries;
CREATE TABLE deliveries (
    delivery_id INTEGER PRIMARY KEY,
    courier     TEXT    NOT NULL,
    minutes     INTEGER NOT NULL
);
INSERT INTO deliveries (delivery_id, courier, minutes) VALUES
    (1,  'ana',   22), (2,  'ana',   35), (3,  'ana',   18), (4,  'ana',   22),
    (5,  'ana',   41), (6,  'ana',   27),
    (7,  'ben',   30), (8,  'ben',   30), (9,  'ben',   12), (10, 'ben',   45),
    (11, 'ben',   12), (12, 'ben',   19), (13, 'ben',   60),
    (14, 'chloe', 25),
    (15, 'dev',   40), (16, 'dev',   10), (17, 'dev',   55), (18, 'dev',   10),
    (19, 'dev',   33), (20, 'dev',   47), (21, 'dev',   21), (22, 'dev',   33),
    (23, 'dev',   29), (24, 'dev',   38),
    (25, 'eli',   14), (26, 'eli',   16);

-- Q1: median per courier
WITH ranked AS (
    SELECT courier, minutes,
           ROW_NUMBER() OVER (PARTITION BY courier ORDER BY minutes) AS rn,
           COUNT(*)     OVER (PARTITION BY courier)                  AS n
    FROM deliveries
)
SELECT courier, n, AVG(minutes * 1.0) AS median_minutes
FROM ranked
WHERE rn IN ((n + 1) / 2, (n + 2) / 2)
GROUP BY courier, n
ORDER BY courier;


-- Q2: mode(s) per courier, ties included, only when the top frequency > 1
WITH freq AS (
    SELECT courier, minutes, COUNT(*) AS times
    FROM deliveries
    GROUP BY courier, minutes
), ranked AS (
    SELECT courier, minutes, times,
           MAX(times) OVER (PARTITION BY courier) AS top
    FROM freq
)
SELECT courier, minutes, times
FROM ranked
WHERE times = top AND top > 1
ORDER BY courier, minutes;


-- Q3: nearest-rank p90 per courier and how many deliveries were slower
WITH ranked AS (
    SELECT courier, minutes,
           ROW_NUMBER() OVER (PARTITION BY courier ORDER BY minutes) AS rn,
           COUNT(*)     OVER (PARTITION BY courier)                  AS n
    FROM deliveries
), p90 AS (
    SELECT courier, minutes AS p90_minutes
    FROM ranked
    WHERE rn = (9 * n + 9) / 10
)
SELECT p.courier, p.p90_minutes,
       (SELECT COUNT(*) FROM deliveries d
         WHERE d.courier = p.courier AND d.minutes > p.p90_minutes) AS slower_than_p90
FROM p90 p
ORDER BY p.courier;
