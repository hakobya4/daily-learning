-- Day 43, Task 6 -- SQL: above-average earners, second-highest salary, spread.
--
-- Self-contained. Load with: sqlite3 practice_day43.db < day43-above-average-and-dense-rank.sql
--
-- THE PROBLEM
-- employees(id, name, dept, salary). Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Employees earning MORE than the average salary of their own dept
--     (correlated subquery or join to a per-dept aggregate).
--     Output: name. Order by name.
-- Q2: The employees with the SECOND-HIGHEST DISTINCT salary in each dept
--     (use DENSE_RANK() = 2; ties both appear; depts with only one distinct
--     salary have no row). Output: dept, name, salary. Order by dept, name.
-- Q3: For depts with at least 2 employees: the salary spread (max - min).
--     Output: dept, spread. Order by spread DESC, dept.
--
-- Expected results for the data below:
--   Q1: ann, cy, eli
--   Q2: eng|gus|90   and   ops|dee|40
--   Q3: ops|30   then   eng|20

CREATE TABLE employees (id INTEGER, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'ann','eng',100),(2,'bo','eng',80),(3,'cy','eng',100),
 (4,'dee','ops',40),(5,'eli','ops',70),(6,'fay','hr',60),(7,'gus','eng',90);

-- Q1
-- TODO

-- Q2
-- TODO

-- Q3
-- TODO
