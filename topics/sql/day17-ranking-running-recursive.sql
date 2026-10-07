-- Day 17, Task 1 -- SQL: ranking per group, running totals, recursive CTE, HAVING.
--
-- Self-contained. Load with: sqlite3 practice_day17.db < day17-ranking-running-recursive.sql
--
-- THE PROBLEM
-- sales(id, rep, region, sold_on, amount) and staff(id, name, boss_id).
-- Write 5 queries. Nothing is pre-solved.
--
-- Q1: Top sale per region: (region, rep, amount) -- the single largest sale
--     in each region (use ROW_NUMBER() OVER (PARTITION BY region ORDER BY
--     amount DESC)). Order by region.
-- Q2: Running total per rep ordered by sold_on, id:
--     (rep, sold_on, amount, running_total). Order by rep, sold_on, id.
-- Q3: Reps whose average sale is above the overall average sale:
--     (rep, avg_amount) with avg_amount rounded to 2 decimals. Order by rep.
-- Q4: Management chain: with a recursive CTE, list every employee under
--     'Ada' (directly or indirectly) as (name, depth) where direct reports
--     have depth 1. Order by depth, name.
-- Q5: Regions with at least 2 distinct reps AND total amount >= 500:
--     (region, reps, total). Order by region.

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS staff;
CREATE TABLE sales (id INTEGER PRIMARY KEY, rep TEXT NOT NULL, region TEXT NOT NULL, sold_on TEXT NOT NULL, amount INTEGER NOT NULL);
CREATE TABLE staff (id INTEGER PRIMARY KEY, name TEXT NOT NULL, boss_id INTEGER);

INSERT INTO sales (id, rep, region, sold_on, amount) VALUES
 (1,'zed','east','2026-01-03',120),(2,'zed','east','2026-01-09',80),
 (3,'amy','east','2026-01-05',300),(4,'amy','west','2026-01-06',50),
 (5,'bob','west','2026-01-07',410),(6,'bob','west','2026-01-07',90),
 (7,'cat','north','2026-01-08',60),(8,'cat','north','2026-01-12',40),
 (9,'zed','west','2026-01-15',200);
INSERT INTO staff (id, name, boss_id) VALUES
 (1,'Ada',NULL),(2,'Ben',1),(3,'Cy',1),(4,'Di',2),(5,'Eve',2),(6,'Fay',4),(7,'Gus',NULL),(8,'Hal',7);

-- Q1:
-- TODO: replace this line with your query;

-- Q2:
-- TODO: replace this line with your query;

-- Q3:
-- TODO: replace this line with your query;

-- Q4:
-- TODO: replace this line with your query;

-- Q5:
-- TODO: replace this line with your query;
