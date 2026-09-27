-- Day 6, Task 1 -- SQL: recursive CTEs (org chart traversal).
-- Schema: day6-schema.sql (employees_org_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: Using a RECURSIVE CTE, list every employee who reports to Malik
-- (id 2), DIRECTLY OR INDIRECTLY, along with how many levels below
-- Malik they are (a direct report is depth 1, a report of a report is
-- depth 2, and so on). Order by depth, then name.
WITH RECURSIVE reports(id, name, depth) AS (
    SELECT id, name, 1
    FROM employees_org_sql
    WHERE manager_id = 2
    UNION ALL
    SELECT e.id, e.name, r.depth + 1
    FROM employees_org_sql e
    JOIN reports r ON e.manager_id = r.id
)
SELECT id, name, depth
FROM reports
ORDER BY depth, name;


-- Q2: Using a RECURSIVE CTE, compute how many levels below the CEO
-- (Rosa, id 1, the row with a NULL manager_id) EVERY employee is --
-- Rosa herself is depth 0. Order by depth, then name.
WITH RECURSIVE depths(id, name, depth) AS (
    SELECT id, name, 0
    FROM employees_org_sql
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, d.depth + 1
    FROM employees_org_sql e
    JOIN depths d ON e.manager_id = d.id
)
SELECT id, name, depth
FROM depths
ORDER BY depth, name;
