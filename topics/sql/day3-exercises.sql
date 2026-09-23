-- Day 3 -- SQL exercises: self-joins, HAVING, and NULL-safe filters.
-- Schema: day3-schema.sql (employees_sql, departments_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: List each employee's name alongside their manager's name. Show
-- NULL (or blank) for employees who have no manager.
-- TODO: write this query (self-join on employees_sql).


-- Q2: For each department, show the department name and the average
-- salary of employees in it, highest average first.
-- TODO: write this query.


-- Q3: List departments that have MORE THAN ONE employee earning above
-- $80,000.
-- TODO: write this query (GROUP BY + HAVING with a filtered condition).


-- Q4: List every employee who is a manager (i.e., appears as someone
-- else's manager_id), along with how many direct reports they have.
-- TODO: write this query.


-- Q5: List employees who earn MORE than their own manager. (Chris and
-- anyone with no manager should not appear.)
-- TODO: write this query (self-join, compare salaries).
