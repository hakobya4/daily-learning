-- Day 6, Task 1 -- SQL: recursive CTEs (org chart traversal).
-- Schema: day6-schema.sql (employees_org_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: Using a RECURSIVE CTE, list every employee who reports to Malik
-- (id 2), DIRECTLY OR INDIRECTLY, along with how many levels below
-- Malik they are (a direct report is depth 1, a report of a report is
-- depth 2, and so on). Order by depth, then name.
-- TODO: write this query (WITH RECURSIVE reports(id, name, depth) AS (...)).


-- Q2: Using a RECURSIVE CTE, compute how many levels below the CEO
-- (Rosa, id 1, the row with a NULL manager_id) EVERY employee is --
-- Rosa herself is depth 0. Order by depth, then name.
-- TODO: write this query.
