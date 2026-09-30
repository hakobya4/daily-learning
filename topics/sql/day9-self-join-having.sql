-- Day 9, Task 2 -- SQL: self-join and HAVING.
--
-- Self-contained. Load with: sqlite3 practice_day9b.db < day9-self-join-having.sql
--
-- THE PROBLEM
-- staff_sql has a manager_id pointing back at another row in the same
-- table (NULL for the top boss). Write 3 queries. Nothing pre-solved.
--
-- Q1: List each employee with their manager's name (column names:
--     employee, manager). Employees with no manager must still appear
--     with manager NULL. Order by employee.
-- Q2: List managers who have 2 or more direct reports: manager name and
--     report_count. Use GROUP BY + HAVING. Order by manager.
-- Q3: Find pairs of employees who share the same manager and the same
--     salary (each pair once: use a.id < b.id). Show a_name, b_name.
--
-- HINT: a self-join is just the same table joined to itself under two
-- aliases; LEFT JOIN keeps the boss row in Q1.

DROP TABLE IF EXISTS staff_sql;
CREATE TABLE staff_sql (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER REFERENCES staff_sql(id),
    salary     INTEGER NOT NULL
);
INSERT INTO staff_sql (id, name, manager_id, salary) VALUES
    (1, 'Zoe',   NULL, 200),
    (2, 'Yan',   1,    120),
    (3, 'Xia',   1,    120),
    (4, 'Wes',   2,    80),
    (5, 'Vic',   2,    90),
    (6, 'Uma',   3,    80);

-- Q1: employee with manager name (LEFT JOIN keeps the boss)
SELECT e.name AS employee, m.name AS manager
FROM staff_sql e
LEFT JOIN staff_sql m ON e.manager_id = m.id
ORDER BY employee;

-- Q2: managers with 2+ direct reports
SELECT m.name AS manager, COUNT(*) AS report_count
FROM staff_sql e
JOIN staff_sql m ON e.manager_id = m.id
GROUP BY m.id, m.name
HAVING COUNT(*) >= 2
ORDER BY manager;

-- Q3: pairs with same manager and same salary (each pair once)
SELECT a.name AS a_name, b.name AS b_name
FROM staff_sql a
JOIN staff_sql b
  ON a.manager_id = b.manager_id
 AND a.salary = b.salary
 AND a.id < b.id
ORDER BY a_name, b_name;
