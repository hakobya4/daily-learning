-- Day 11, Task 1 -- SQL: top-N per group, percent of total, and median.
--
-- Self-contained. Load with: sqlite3 practice_day11.db < day11-top-n-and-median.sql
--
-- THE PROBLEM
-- employees holds name, dept and salary. Write 4 queries. Nothing is
-- pre-solved.
--
-- Q1: The top 2 earners in each dept (dept, name, salary), highest
--     first; on salary ties include all tied rows at rank <= 2 (use
--     DENSE_RANK). Order by dept, salary DESC, name.
-- Q2: For each employee, their salary as a percentage of their dept's
--     total, rounded to 1 decimal (name, dept, pct_of_dept). Use a
--     window SUM, not a join. Order by dept, name.
-- Q3: The MEDIAN salary per dept (dept, median_salary). For an even
--     count, average the two middle values. SQLite has no MEDIAN():
--     use ROW_NUMBER and COUNT windows, then filter the middle row(s).
-- Q4: Employees who earn more than the average of THEIR OWN dept
--     (name, dept, salary, dept_avg rounded to 0 decimals).
--
-- HINT for Q3: rows where rn IN ((cnt+1)/2, (cnt+2)/2) (integer
-- division) are the middle one or two rows; AVG over them.

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    name   TEXT NOT NULL,
    dept   TEXT NOT NULL,
    salary INTEGER NOT NULL
);
INSERT INTO employees (name, dept, salary) VALUES
    ('Ana',   'eng',   120), ('Ben',   'eng',   100), ('Cleo',  'eng',   100),
    ('Dev',   'eng',    90), ('Eli',   'ops',    70), ('Fay',   'ops',    80),
    ('Gus',   'ops',    60), ('Hana',  'hr',     65), ('Ivo',   'hr',     65),
    ('Jo',    'hr',     75);

-- Q1
SELECT dept, name, salary
FROM (
    SELECT dept, name, salary,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
)
WHERE rnk <= 2
ORDER BY dept, salary DESC, name;

-- Q2
SELECT name, dept,
       ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY dept), 1) AS pct_of_dept
FROM employees
ORDER BY dept, name;

-- Q3
SELECT dept, AVG(salary) AS median_salary
FROM (
    SELECT dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary, name) AS rn,
           COUNT(*)     OVER (PARTITION BY dept) AS cnt
    FROM employees
)
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
GROUP BY dept
ORDER BY dept;

-- Q4
SELECT name, dept, salary, ROUND(dept_avg, 0) AS dept_avg
FROM (
    SELECT name, dept, salary,
           AVG(salary) OVER (PARTITION BY dept) AS dept_avg
    FROM employees
)
WHERE salary > dept_avg
ORDER BY dept, salary DESC, name;
