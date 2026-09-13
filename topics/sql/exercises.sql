-- Day 2 -- SQL exercises: joins, aggregation, and NULL handling.
--
-- Setup: sqlite3 practice.db < schema.sql
-- Then either paste these one at a time into `sqlite3 practice.db`,
-- or fill them in here and run: sqlite3 practice.db < exercises.sql
--
-- Each query below is a TODO. Expected results are given so you can
-- check your own work without a solution being handed to you. Don't
-- move to the next one until your query's actual output matches.

-- Q1: List the name of every customer who lives in 'Toronto'.
-- Expected: 3 rows -- Alice, Bob, Erin (order doesn't matter).
-- TODO: write this query.


-- Q2: For each customer who has placed at least one order, show their
-- name and their TOTAL amount spent, highest spender first. Customers
-- with zero orders should NOT appear (this is the difference between
-- INNER JOIN and LEFT JOIN -- think about which one you need and why).
-- Expected: 4 rows -- Dave 500.00, Bob 300.00, Alice 225.50, Carol 75.25.
-- TODO: write this query (JOIN + GROUP BY + SUM, ORDER BY total DESC).


-- Q3: List every customer who has NEVER placed an order.
-- Expected: 1 row -- Erin.
-- Hint: this needs a LEFT JOIN from customers to orders, then filtering
-- for rows where the order side is NULL -- an INNER JOIN can never
-- produce this answer, since it only keeps rows that matched.
-- TODO: write this query.


-- Q4: For each customer who has ordered, show their name and the date
-- of their MOST RECENT order.
-- Expected: 4 rows -- Alice 2026-05-01, Bob 2026-02-20,
--           Carol 2026-01-15, Dave 2026-04-01.
-- Hint: MAX(order_date) grouped by customer works here because the
-- dates are in 'YYYY-MM-DD' format, which sorts correctly as text.
-- TODO: write this query.


-- Q5: List customers whose TOTAL spending is above the AVERAGE total
-- spending across all customers who have ordered.
-- Expected: 2 rows -- Bob (300.00) and Dave (500.00).
-- (Average of the four totals from Q2 is 275.1875; Alice's 225.50 and
-- Carol's 75.25 both fall below it.)
-- Hint: you likely need a subquery or CTE that computes per-customer
-- totals first, then compares each total against the AVG() of that
-- same set.
-- TODO: write this query.
