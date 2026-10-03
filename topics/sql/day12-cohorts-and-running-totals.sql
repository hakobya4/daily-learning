-- Day 12, Task 1 -- SQL: running totals, month-over-month, quartiles, first-order cohorts.
--
-- Self-contained. Load with: sqlite3 practice_day12.db < day12-cohorts-and-running-totals.sql
--
-- THE PROBLEM
-- orders holds id, customer, order_date (YYYY-MM-DD) and amount.
-- Write 4 queries. Nothing is pre-solved.
--
-- Q1: Running total of amount per customer in date order
--     (customer, order_date, amount, running_total). Break date ties
--     by id. Order by customer, order_date, id.
-- Q2: Monthly revenue with change vs. the previous month
--     (month 'YYYY-MM', revenue, prev_revenue, change). prev_revenue
--     and change are NULL for the first month. Use LAG over a
--     grouped subquery/CTE. Order by month.
-- Q3: Split orders into 4 spend quartiles with NTILE(4) over amount
--     (id, amount, quartile). Ties broken by id. Order by id.
-- Q4: First-order cohort: for each customer's first order month, how
--     many customers started then, and how many of them ordered again
--     in a LATER month (cohort_month, customers, returned).
--     Order by cohort_month.
--
-- HINT for Q4: CTE of (customer, first_month); join to distinct order
-- months where month > first_month; COUNT(DISTINCT ...).

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id         INTEGER PRIMARY KEY,
    customer   TEXT NOT NULL,
    order_date TEXT NOT NULL,
    amount     INTEGER NOT NULL
);
INSERT INTO orders (id, customer, order_date, amount) VALUES
    (1,  'ann', '2026-01-05', 40), (2,  'bob', '2026-01-09', 25),
    (3,  'ann', '2026-01-20', 10), (4,  'cy',  '2026-02-02', 60),
    (5,  'bob', '2026-02-14', 35), (6,  'dee', '2026-02-14', 15),
    (7,  'ann', '2026-03-01', 50), (8,  'cy',  '2026-03-03', 20),
    (9,  'eve', '2026-03-10', 90), (10, 'dee', '2026-03-22', 30);

-- Q1

-- Q2

-- Q3

-- Q4
