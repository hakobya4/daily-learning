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

-- Q1: TODO: write this query


-- Q2: TODO: write this query


-- Q3: TODO: write this query

