-- Day 50, Task 7 -- SQL: top-per-group with ties, self-join, HAVING vs overall average.
--
-- Self-contained. Load with: sqlite3 practice_day50.db < day50-employees.sql
--
-- THE PROBLEM
-- employees(id, name, dept, salary, manager_id); manager_id is NULL for the top of a team.
-- Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Highest-paid employee(s) per department, ties all included. Output: dept, name.
--     Order by dept, name.   Hint: RANK() OVER (PARTITION BY dept ORDER BY salary DESC).
-- Q2: Employees who earn more than their own manager. Output: name, manager. Order by name.
-- Q3: Departments whose average salary is above the company-wide average salary.
--     Output: dept, avg_salary (ROUND to 2 decimals). Order by dept.
-- Q4: Managers with 2 or more direct reports. Output: name, reports. Order by name.
--
-- Expected results for the data below:
--   Q1: eng|bob  hr|gus  hr|hal  ops|eve
--   Q2: bob|ann  eve|dan
--   Q3: eng|103.33
--   Q4: ann|2  dan|2

CREATE TABLE employees (id INTEGER, name TEXT, dept TEXT, salary INTEGER, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'ann','eng',100,NULL),
 (2,'bob','eng',120,1),
 (3,'cat','eng',90,1),
 (4,'dan','ops',70,NULL),
 (5,'eve','ops',80,4),
 (6,'fay','ops',60,4),
 (7,'gus','hr',65,NULL),
 (8,'hal','hr',65,7);

-- Q1

-- Q2

-- Q3

-- Q4
