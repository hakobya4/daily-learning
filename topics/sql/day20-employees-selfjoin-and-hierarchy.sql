-- Day 20, Task 1 -- SQL: self-join, share of total, NOT EXISTS, recursive depth, DENSE_RANK.
--
-- Self-contained. Load with: sqlite3 practice_day20.db < day20-employees-selfjoin-and-hierarchy.sql
--
-- THE PROBLEM
-- departments(id, name) and employees(id, name, dept_id, manager_id, salary).
-- manager_id is NULL for the top boss. Write 5 queries. Nothing is pre-solved.
--
-- Q1: Employees who earn more than their own manager (self-join):
--     (name, salary, manager_name, manager_salary). Order by name.
-- Q2: Each department's share of the company payroll:
--     (dept, total_salary, pct) where pct = ROUND(100.0 * total / company_total, 1).
--     Order by pct DESC, dept.
-- Q3: Employees with no direct reports, using NOT EXISTS: (name). Order by name.
-- Q4: Management depth via a recursive CTE: (name, depth), boss = depth 0,
--     direct reports of the boss = 1, and so on. Order by depth, name.
-- Q5: The employee(s) with the second-highest DISTINCT salary in each
--     department (DENSE_RANK = 2): (dept, name, salary). Departments with
--     only one distinct salary do not appear. Order by dept, name.

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept_id INTEGER NOT NULL, manager_id INTEGER, salary INTEGER NOT NULL);

INSERT INTO departments (id, name) VALUES (1,'Engineering'),(2,'Sales'),(3,'Support');
INSERT INTO employees (id, name, dept_id, manager_id, salary) VALUES
 (1,'Ada',1,NULL,200),
 (2,'Bo',1,1,150),
 (3,'Cy',1,2,160),
 (4,'Di',1,2,150),
 (5,'Eli',2,1,120),
 (6,'Flo',2,5,130),
 (7,'Gus',2,5,90),
 (8,'Hal',3,1,80),
 (9,'Ivy',3,8,80),
 (10,'Jo',3,8,70);

-- Write your queries below:

-- Q1
SELECT e.name, e.salary, m.name AS manager_name, m.salary AS manager_salary
FROM employees e
JOIN employees m ON m.id = e.manager_id
WHERE e.salary > m.salary
ORDER BY e.name;


-- Q2
SELECT d.name AS dept,
       SUM(e.salary) AS total_salary,
       ROUND(100.0 * SUM(e.salary) / (SELECT SUM(salary) FROM employees), 1) AS pct
FROM employees e
JOIN departments d ON d.id = e.dept_id
GROUP BY d.id, d.name
ORDER BY pct DESC, dept;


-- Q3
SELECT e.name
FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM employees r WHERE r.manager_id = e.id)
ORDER BY e.name;


-- Q4
WITH RECURSIVE chain(id, name, depth) AS (
  SELECT id, name, 0 FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, c.depth + 1
  FROM employees e
  JOIN chain c ON e.manager_id = c.id
)
SELECT name, depth FROM chain ORDER BY depth, name;


-- Q5
SELECT dept, name, salary
FROM (
  SELECT d.name AS dept, e.name AS name, e.salary AS salary,
         DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
  FROM employees e
  JOIN departments d ON d.id = e.dept_id
)
WHERE rnk = 2
ORDER BY dept, name;

