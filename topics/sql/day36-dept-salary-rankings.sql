-- Day 36, Task 1 -- SQL: department salary rankings.
--
-- Self-contained. Load with: sqlite3 practice_day36.db < day36-dept-salary-rankings.sql
--
-- THE PROBLEM
-- departments(id, name) and employees(id, name, dept_id, salary). Write 3
-- queries below the data. Nothing pre-solved.
--
-- Q1: The SECOND highest distinct salary in each department (departments
--     with fewer than 2 distinct salaries are omitted). Output: dept, salary.
--     Order by dept.
-- Q2: Employees earning strictly more than the average salary of their own
--     department. Output: name, dept, salary. Order by dept, name.
-- Q3: Departments with no employees at all. Output: dept. Order by dept.
--
-- HINT: DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC);
-- AVG(salary) OVER (PARTITION BY dept_id); LEFT JOIN ... WHERE e.id IS NULL.
--
-- Expected results for the data below:
--   Q1: eng 90 / ops 50
--   Q2: eng|cleo|100, eng|dan|90, ops|gus|60
--   Q3: legal

CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (1,'eng'),(2,'ops'),(3,'hr'),(4,'legal');
INSERT INTO employees VALUES
  (1,'ann',1,70),(2,'bob',1,70),(3,'cleo',1,100),(4,'dan',1,90),
  (5,'eve',2,50),(6,'fay',2,40),(7,'gus',2,60),
  (8,'hal',3,55);

-- TODO: Q1


-- TODO: Q2


-- TODO: Q3
