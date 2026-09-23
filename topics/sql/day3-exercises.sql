-- Day 3 -- SQL exercises: self-joins, HAVING, and NULL-safe filters.
-- Schema: day3-schema.sql (employees_sql, departments_sql)
--
-- Q1: List each employee's name alongside their manager's name. Show
-- NULL (or blank) for employees who have no manager.
SELECT
    e.name AS employee_name,
    m.name AS manager_name
FROM employees_sql e
LEFT JOIN employees_sql m ON e.manager_id = m.id;


-- Q2: For each department, show the department name and the average
-- salary of employees in it, highest average first.
SELECT
    d.name AS department_name,
    AVG(e.salary) AS avg_salary
FROM departments_sql d
JOIN employees_sql e ON e.department_id = d.id
GROUP BY d.id, d.name
ORDER BY avg_salary DESC;


-- Q3: List departments that have MORE THAN ONE employee earning above
-- $80,000.
SELECT
    d.name AS department_name,
    COUNT(*) AS high_earners
FROM departments_sql d
JOIN employees_sql e ON e.department_id = d.id
WHERE e.salary > 80000
GROUP BY d.id, d.name
HAVING COUNT(*) > 1;


-- Q4: List every employee who is a manager (i.e., appears as someone
-- else's manager_id), along with how many direct reports they have.
SELECT
    m.name AS manager_name,
    COUNT(e.id) AS direct_reports
FROM employees_sql m
JOIN employees_sql e ON e.manager_id = m.id
GROUP BY m.id, m.name;


-- Q5: List employees who earn MORE than their own manager. (Chris and
-- anyone with no manager should not appear.)
SELECT
    e.name AS employee_name,
    e.salary AS employee_salary,
    m.name AS manager_name,
    m.salary AS manager_salary
FROM employees_sql e
JOIN employees_sql m ON e.manager_id = m.id
WHERE e.salary > m.salary;
