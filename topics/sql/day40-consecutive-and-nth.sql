-- Day 40, Task 6 -- SQL: second-highest, above-average, share of total.
--
-- Self-contained. Load with: sqlite3 practice_day40.db < day40-consecutive-and-nth.sql
--
-- THE PROBLEM
-- emp(id, name, dept, salary). Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: The 2nd highest DISTINCT salary in each dept (depts with fewer than 2
--     distinct salaries are omitted). Output: dept, salary. Order by dept.
-- Q2: Employees earning strictly more than the average salary of their OWN dept.
--     Output: name. Order by name.
-- Q3: For each employee, their salary as a percent of the dept total, rounded
--     to 1 decimal. Output: name, pct. Order by dept, salary DESC, name.
--
-- HINT: Q1 DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) in a CTE;
-- Q2 window AVG(salary) OVER (PARTITION BY dept) or correlated subquery;
-- Q3 ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY dept), 1).
-- Expected results for the data below:
--   Q1: eng|110, ops|60
--   Q2: Ann, Bob, Cy, Fay
--   Q3: Ann|29.3, Bob|29.3, Cy|26.8, Di|14.6, Eve|100.0, Fay|33.3, Gus|25.0, Hal|25.0, Ivy|16.7

CREATE TABLE emp (id INTEGER, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO emp VALUES
  (1,'Ann','eng',120),(2,'Bob','eng',120),(3,'Cy','eng',110),(4,'Di','eng',60),
  (5,'Eve','hr',50),
  (6,'Fay','ops',80),(7,'Gus','ops',60),(8,'Hal','ops',60),(9,'Ivy','ops',40);

-- Q1

-- Q2

-- Q3
