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


-- Q2


-- Q3


-- Q4


-- Q5

