-- Day 59, Task 3 -- SQL: a strictly ordered, time-boxed conversion funnel.
--
-- Self-contained. Load with: sqlite3 practice_day59.db < day59-ordered-funnel-conversion.sql
-- (needs window functions: SQLite >= 3.25, or PostgreSQL / MySQL 8 with the date math
-- adapted). No sqlite3 CLI? python3 -c "import sqlite3; ..." runs it just as well.
--
-- THE PROBLEM
-- events(event_id, user_id, ts, event) logs what users did; ts is 'YYYY-MM-DD HH:MM'
-- and event is one of 'view', 'cart', 'checkout', 'purchase'.
-- The funnel is view -> cart -> checkout -> purchase, measured per user like this:
--   step 1 (view)     = the user's FIRST view (users with no view are not in the funnel)
--   step 2 (cart)     = the earliest cart     STRICTLY AFTER the step-1 time
--   step 3 (checkout) = the earliest checkout STRICTLY AFTER the step-2 time
--   step 4 (purchase) = the earliest purchase STRICTLY AFTER the step-3 time
-- and every step must happen within 72 hours (inclusive) of the step-1 time. A user who
-- misses a step does not reach any later step, even if later events exist.
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: step_no, step, users (how many users reached it), pct_of_viewers
--     = ROUND(100.0 * users / users_at_step_1, 1), pct_of_previous = the same relative to
--     the previous step (NULL for step 1; use LAG). All four steps, even with 0 users.
--     Hint: one CTE per step with a correlated MIN(ts) subquery (or a LEFT JOIN +
--     GROUP BY), then UNION ALL four counts.
-- Q2: For users who reached step 4: user_id, minutes_to_purchase (whole minutes from
--     step 1 to step 4), ordered by minutes_to_purchase DESC, then user_id.
--     Hint (SQLite): CAST(ROUND((julianday(b) - julianday(a)) * 1440) AS INTEGER).
-- Q3: Abandoned carts, independent of the funnel: users whose LAST cart event has no
--     purchase at or after it (same minute counts as "after"). Output user_id,
--     last_cart_ts, ordered by user_id.
--
-- Expected results for the data below:
--   Q1: 1|view|8|100.0|NULL
--       2|cart|6|75.0|75.0
--       3|checkout|5|62.5|83.3
--       4|purchase|3|37.5|60.0
--   Q2: 5|2985
--       1|120
--       7|65
--   Q3: 2|2026-11-01 12:00
--       3|2026-11-02 10:05
--       5|2026-11-08 12:00

CREATE TABLE events (event_id INTEGER PRIMARY KEY, user_id INTEGER, ts TEXT, event TEXT);
INSERT INTO events VALUES
 (1,  1, '2026-11-01 09:00', 'view'),      -- u1: clean full funnel in 2 hours
 (2,  1, '2026-11-01 09:10', 'cart'),
 (3,  1, '2026-11-01 10:00', 'checkout'),
 (4,  1, '2026-11-01 11:00', 'purchase'),
 (5,  2, '2026-11-01 12:00', 'cart'),      -- u2: cart BEFORE any view does not count
 (6,  2, '2026-11-02 08:00', 'view'),
 (7,  2, '2026-11-02 08:30', 'checkout'),  --     checkout without a cart after the view
 (8,  3, '2026-11-02 10:00', 'view'),      -- u3: reaches checkout, never buys
 (9,  3, '2026-11-02 10:05', 'cart'),
 (10, 3, '2026-11-03 09:00', 'checkout'),
 (11, 4, '2026-11-03 07:00', 'view'),      -- u4: buys, but 4 days after the view
 (12, 4, '2026-11-03 07:20', 'cart'),
 (13, 4, '2026-11-04 20:00', 'checkout'),
 (14, 4, '2026-11-07 07:01', 'purchase'),
 (15, 5, '2026-11-04 15:00', 'view'),      -- u5: two views; funnel measured from the FIRST
 (16, 5, '2026-11-06 15:00', 'view'),
 (17, 5, '2026-11-06 15:30', 'cart'),
 (18, 5, '2026-11-06 16:00', 'checkout'),
 (19, 5, '2026-11-06 16:45', 'purchase'),
 (20, 5, '2026-11-08 12:00', 'cart'),      --     ...and a later cart with no purchase after it
 (21, 6, '2026-11-05 11:00', 'view'),      -- u6: just looking
 (22, 7, '2026-11-05 13:00', 'view'),      -- u7: cart, then purchase without checkout,
 (23, 7, '2026-11-05 13:10', 'cart'),      --     then a proper checkout + purchase
 (24, 7, '2026-11-05 13:15', 'purchase'),
 (25, 7, '2026-11-05 14:00', 'checkout'),
 (26, 7, '2026-11-05 14:05', 'purchase'),
 (27, 8, '2026-11-06 09:00', 'view'),      -- u8: cart and checkout at the SAME minute
 (28, 8, '2026-11-06 09:30', 'cart'),
 (29, 8, '2026-11-06 09:30', 'checkout'),
 (30, 8, '2026-11-06 09:45', 'purchase');

-- Q1
WITH s1 AS (
  SELECT user_id, MIN(ts) AS t1 FROM events WHERE event = 'view' GROUP BY user_id
), s2 AS (
  SELECT s1.user_id, s1.t1,
         (SELECT MIN(e.ts) FROM events e
           WHERE e.user_id = s1.user_id AND e.event = 'cart' AND e.ts > s1.t1
             AND julianday(e.ts) <= julianday(s1.t1) + 3) AS t2
  FROM s1
), s3 AS (
  SELECT s2.user_id, s2.t1, s2.t2,
         (SELECT MIN(e.ts) FROM events e
           WHERE e.user_id = s2.user_id AND e.event = 'checkout' AND e.ts > s2.t2
             AND julianday(e.ts) <= julianday(s2.t1) + 3) AS t3
  FROM s2 WHERE s2.t2 IS NOT NULL
), s4 AS (
  SELECT s3.user_id, s3.t1,
         (SELECT MIN(e.ts) FROM events e
           WHERE e.user_id = s3.user_id AND e.event = 'purchase' AND e.ts > s3.t3
             AND julianday(e.ts) <= julianday(s3.t1) + 3) AS t4
  FROM s3 WHERE s3.t3 IS NOT NULL
), counts AS (
  SELECT 1 AS step_no, 'view' AS step, COUNT(*) AS users FROM s1
  UNION ALL SELECT 2, 'cart',     COUNT(t2) FROM s2
  UNION ALL SELECT 3, 'checkout', COUNT(t3) FROM s3
  UNION ALL SELECT 4, 'purchase', COUNT(t4) FROM s4
)
SELECT step_no, step, users,
       ROUND(100.0 * users / NULLIF((SELECT users FROM counts WHERE step_no = 1), 0), 1)
         AS pct_of_viewers,
       ROUND(100.0 * users / NULLIF(LAG(users) OVER (ORDER BY step_no), 0), 1)
         AS pct_of_previous
FROM counts
ORDER BY step_no;

-- Q2
WITH s1 AS (
  SELECT user_id, MIN(ts) AS t1 FROM events WHERE event = 'view' GROUP BY user_id
), s2 AS (
  SELECT s1.user_id, s1.t1,
         (SELECT MIN(e.ts) FROM events e
           WHERE e.user_id = s1.user_id AND e.event = 'cart' AND e.ts > s1.t1
             AND julianday(e.ts) <= julianday(s1.t1) + 3) AS t2
  FROM s1
), s3 AS (
  SELECT s2.user_id, s2.t1,
         (SELECT MIN(e.ts) FROM events e
           WHERE e.user_id = s2.user_id AND e.event = 'checkout' AND e.ts > s2.t2
             AND julianday(e.ts) <= julianday(s2.t1) + 3) AS t3
  FROM s2 WHERE s2.t2 IS NOT NULL
), s4 AS (
  SELECT s3.user_id, s3.t1,
         (SELECT MIN(e.ts) FROM events e
           WHERE e.user_id = s3.user_id AND e.event = 'purchase' AND e.ts > s3.t3
             AND julianday(e.ts) <= julianday(s3.t1) + 3) AS t4
  FROM s3 WHERE s3.t3 IS NOT NULL
)
SELECT user_id,
       CAST(ROUND((julianday(t4) - julianday(t1)) * 1440) AS INTEGER) AS minutes_to_purchase
FROM s4
WHERE t4 IS NOT NULL
ORDER BY minutes_to_purchase DESC, user_id;

-- Q3
WITH last_cart AS (
  SELECT user_id, MAX(ts) AS last_cart_ts FROM events WHERE event = 'cart' GROUP BY user_id
)
SELECT lc.user_id, lc.last_cart_ts
FROM last_cart lc
WHERE NOT EXISTS (
  SELECT 1 FROM events e
  WHERE e.user_id = lc.user_id AND e.event = 'purchase' AND e.ts >= lc.last_cart_ts
)
ORDER BY lc.user_id;
