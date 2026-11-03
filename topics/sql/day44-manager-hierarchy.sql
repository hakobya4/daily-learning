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
-- TODO: write the query

-- Q2
-- TODO: write the query

-- Q3
-- TODO: write the query
