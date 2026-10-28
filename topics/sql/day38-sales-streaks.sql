-- Day 38, Task 1 -- SQL: running totals, day-over-day growth and streaks.
--
-- Self-contained. Load with: sqlite3 practice_day38.db < day38-sales-streaks.sql
--
-- THE PROBLEM
-- sales(day, amount) with day as an ISO date string (one row per day, some days missing).
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Running total of amount ordered by day. Output: day, amount, running_total.
-- Q2: Days where amount is strictly greater than the previous ROW's amount
--     (by day order). Output: day, amount, prev_amount. Order by day.
-- Q3: Streaks of CONSECUTIVE calendar days (gaps-and-islands). Output:
--     streak_start, streak_end, days. Order by streak_start.
--
-- HINT: Q1/Q2 use window functions SUM() OVER / LAG(); Q3: day minus ROW_NUMBER()
-- (e.g. julianday(day) - ROW_NUMBER() OVER (ORDER BY day)) is constant within an island.
--
-- Expected results for the data below:
--   Q1: 2026-01-01|10|10, 2026-01-02|20|30, 2026-01-03|15|45, 2026-01-05|40|85, 2026-01-06|5|90, 2026-01-09|30|120
--   Q2: 2026-01-02|20|10, 2026-01-05|40|15, 2026-01-09|30|5
--   Q3: 2026-01-01|2026-01-03|3, 2026-01-05|2026-01-06|2, 2026-01-09|2026-01-09|1

CREATE TABLE sales (day TEXT, amount INTEGER);
INSERT INTO sales VALUES
  ('2026-01-01',10),('2026-01-02',20),('2026-01-03',15),
  ('2026-01-05',40),('2026-01-06',5),('2026-01-09',30);

-- Q1
SELECT day, amount, SUM(amount) OVER (ORDER BY day) AS running_total
FROM sales
ORDER BY day;

-- Q2
SELECT day, amount, prev_amount
FROM (
  SELECT day, amount, LAG(amount) OVER (ORDER BY day) AS prev_amount
  FROM sales
)
WHERE prev_amount IS NOT NULL AND amount > prev_amount
ORDER BY day;

-- Q3
SELECT MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS days
FROM (
  SELECT day, julianday(day) - ROW_NUMBER() OVER (ORDER BY day) AS grp
  FROM sales
)
GROUP BY grp
ORDER BY streak_start;
