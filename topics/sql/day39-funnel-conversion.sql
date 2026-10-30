-- Day 39, Task 6 -- SQL: funnel conversion.
--
-- Self-contained. Load with: sqlite3 practice_day39.db < day39-funnel-conversion.sql
--
-- THE PROBLEM
-- events(user_id, step, ts) logs funnel steps 'visit' -> 'cart' -> 'purchase'
-- (ts is an integer time). A user may log a step more than once or skip steps.
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Distinct users per step. Output: step, users. Order by users DESC, step.
-- Q2: Users who reached 'cart' but never 'purchase'. Output: user_id. Order by user_id.
-- Q3: Users who completed the whole funnel IN ORDER (their first visit < their
--     first cart < their first purchase by ts). Output: user_id. Order by user_id.
--
-- HINT: Q1 COUNT(DISTINCT); Q2 NOT EXISTS / EXCEPT; Q3 GROUP BY user_id with
-- MIN(CASE WHEN step='visit' THEN ts END) etc. and compare in HAVING.
-- Expected results for the data below:
--   Q1: visit|5, cart|4, purchase|3
--   Q2: 2, 5
--   Q3: 1

CREATE TABLE events (user_id INTEGER, step TEXT, ts INTEGER);
INSERT INTO events VALUES
  (1,'visit',1),(1,'cart',2),(1,'purchase',3),
  (2,'visit',1),(2,'cart',2),(2,'cart',5),
  (3,'visit',1),
  (4,'visit',1),(4,'purchase',2),(4,'cart',3),
  (5,'cart',1),
  (6,'visit',1),(6,'purchase',2);

-- Q1
SELECT step, COUNT(DISTINCT user_id) AS users
FROM events
GROUP BY step
ORDER BY users DESC, step;

-- Q2
SELECT DISTINCT user_id
FROM events e
WHERE step = 'cart'
  AND NOT EXISTS (SELECT 1 FROM events p WHERE p.user_id = e.user_id AND p.step = 'purchase')
ORDER BY user_id;

-- Q3
SELECT user_id
FROM events
GROUP BY user_id
HAVING MIN(CASE WHEN step = 'visit' THEN ts END) < MIN(CASE WHEN step = 'cart' THEN ts END)
   AND MIN(CASE WHEN step = 'cart' THEN ts END) < MIN(CASE WHEN step = 'purchase' THEN ts END)
ORDER BY user_id;
