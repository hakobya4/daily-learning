-- Day 34, Task 1 -- SQL: days between consecutive orders.
--
-- Self-contained. Load with: sqlite3 practice_day34.db < day34-order-gaps.sql
--
-- THE PROBLEM
-- orders(customer, order_date) holds one row per order; order_date is
-- 'YYYY-MM-DD' (no duplicates per customer). Write 3 queries. Nothing
-- pre-solved.
--
-- Q1: For every order, the whole days since that customer's previous order
--     (NULL for a customer's first order). Output: customer, order_date,
--     days_since_prev. Order by customer, order_date.
-- Q2: Average gap in days per customer, rounded to 1 decimal, only for
--     customers with at least two orders. Output: customer, avg_gap.
--     Order by customer.
-- Q3: Customers who ever waited MORE than 30 days between two orders.
--     Output: customer. Order by customer.
--
-- HINT: LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date)
-- and CAST(julianday(a) - julianday(b) AS INTEGER); wrap in a CTE for Q2/Q3.
--
-- Expected results for the data below:
--   Q1: ann 2026-01-05 NULL / ann 2026-01-12 7 / ann 2026-03-01 48 /
--       ann 2026-03-04 3 / bob 2026-02-01 NULL / bob 2026-02-15 14 /
--       bob 2026-03-01 14 / cy 2026-01-20 NULL / dee 2026-01-01 NULL /
--       dee 2026-02-01 31
--   Q2: ann 19.3 / bob 14.0 / dee 31.0
--   Q3: ann / dee

CREATE TABLE orders (customer TEXT, order_date TEXT);
INSERT INTO orders VALUES
  ('ann','2026-01-05'),('ann','2026-01-12'),('ann','2026-03-01'),('ann','2026-03-04'),
  ('bob','2026-02-01'),('bob','2026-02-15'),('bob','2026-03-01'),
  ('cy','2026-01-20'),
  ('dee','2026-01-01'),('dee','2026-02-01');

-- Q1:
SELECT customer, order_date,
       CAST(julianday(order_date) - julianday(
         LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date)) AS INTEGER) AS days_since_prev
FROM orders
ORDER BY customer, order_date;

-- Q2:
WITH gaps AS (
  SELECT customer,
         julianday(order_date) - julianday(
           LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date)) AS gap
  FROM orders
)
SELECT customer, ROUND(AVG(gap), 1) AS avg_gap
FROM gaps
WHERE gap IS NOT NULL
GROUP BY customer
ORDER BY customer;

-- Q3:
WITH gaps AS (
  SELECT customer,
         julianday(order_date) - julianday(
           LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date)) AS gap
  FROM orders
)
SELECT DISTINCT customer
FROM gaps
WHERE gap > 30
ORDER BY customer;
