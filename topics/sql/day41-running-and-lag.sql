-- Day 41, Task 6 -- SQL: running totals, LAG, and best row per group.
--
-- Self-contained. Load with: sqlite3 practice_day41.db < day41-running-and-lag.sql
--
-- THE PROBLEM
-- sales(id, rep, day, amount). Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Running total of amount per rep ordered by day. Output: rep, day, running.
--     Order by rep, day.
-- Q2: Change versus the rep's previous row (by day): amount minus previous amount
--     (NULL on a rep's first row). Output: rep, day, delta. Order by rep, day.
-- Q3: Each rep's biggest sale (ties -> earliest day). Output: rep, day, amount.
--     Order by rep.
--
-- HINT: Q1 SUM() OVER (PARTITION BY rep ORDER BY day); Q2 LAG(amount) OVER (...);
-- Q3 ROW_NUMBER() OVER (PARTITION BY rep ORDER BY amount DESC, day) = 1.
-- Expected results for the data below:
--   Q1: ann|1|10, ann|2|40, ann|3|45, bo|1|7, bo|2|7, bo|4|27
--   Q2: ann|1|NULL, ann|2|20, ann|3|-25, bo|1|NULL, bo|2|-7, bo|4|20
--   Q3: ann|2|30, bo|4|20

CREATE TABLE sales (id INTEGER, rep TEXT, day INTEGER, amount INTEGER);
INSERT INTO sales VALUES
  (1,'ann',1,10),(2,'ann',2,30),(3,'ann',3,5),
  (4,'bo',1,7),(5,'bo',2,0),(6,'bo',4,20);

-- Q1
SELECT rep, day, SUM(amount) OVER (PARTITION BY rep ORDER BY day) AS running
FROM sales
ORDER BY rep, day;

-- Q2
SELECT rep, day, amount - LAG(amount) OVER (PARTITION BY rep ORDER BY day) AS delta
FROM sales
ORDER BY rep, day;

-- Q3
SELECT rep, day, amount FROM (
  SELECT rep, day, amount,
         ROW_NUMBER() OVER (PARTITION BY rep ORDER BY amount DESC, day) AS rn
  FROM sales
) WHERE rn = 1
ORDER BY rep;
