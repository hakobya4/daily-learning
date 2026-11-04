-- Day 44, Task 6 -- SQL: manager hierarchy, depth and total reports.
--
-- Self-contained. Load with: sqlite3 practice_day44.db < day44-manager-hierarchy.sql
--
-- THE PROBLEM
-- employees(id, name, manager_id, salary). Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Employees who earn MORE than their own manager (self-join).
--     Output: name. Order by name.
-- Q2: Depth of every employee in the hierarchy (CEO = 0) with a recursive CTE.
--     Output: name, depth. Order by depth, name.
-- Q3: For every manager, the TOTAL number of reports, direct plus indirect.
--     Only managers with at least 1 report. Output: name, reports.
--     Order by reports DESC, name.
--
-- Expected results for the data below:
--   Q1: cy, fay
--   Q2: ceo|0  ann|1  bob|1  cy|2  dee|2  fay|2  eli|3
--   Q3: ceo|6  ann|3  bob|1  cy|1

CREATE TABLE employees (id INTEGER, name TEXT, manager_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'ceo',NULL,300),(2,'ann',1,200),(3,'bob',1,150),(4,'cy',2,210),
 (5,'dee',2,120),(6,'eli',4,100),(7,'fay',3,160);

-- Q1
SELECT e.name FROM employees e JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary ORDER BY e.name;

-- Q2
WITH RECURSIVE h(id, name, depth) AS (
  SELECT id, name, 0 FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, h.depth + 1 FROM employees e JOIN h ON e.manager_id = h.id
)
SELECT name, depth FROM h ORDER BY depth, name;

-- Q3
WITH RECURSIVE r(root, id) AS (
  SELECT id, id FROM employees
  UNION ALL
  SELECT r.root, e.id FROM employees e JOIN r ON e.manager_id = r.id
)
SELECT m.name, COUNT(*) - 1 AS reports FROM r JOIN employees m ON m.id = r.root
GROUP BY r.root HAVING COUNT(*) - 1 >= 1 ORDER BY reports DESC, m.name;
