-- Day 30, Task 1 -- SQL: new vs. returning customers per month.
--
-- Self-contained. Load with: sqlite3 practice_day30.db < day30-new-vs-returning.sql
--
-- THE PROBLEM
-- orders(customer, order_date) holds one row per order (ISO dates).
-- Write 2 queries. Nothing pre-solved.
--
-- Q1: For every month (YYYY-MM) with at least one order, count the DISTINCT
--     customers who ordered that month, split into new_customers (their very
--     first order ever was that month) and returning_customers (first order
--     was in an earlier month). Output: month, new_customers,
--     returning_customers. Order by month.
-- Q2: For every customer, the number of days between their FIRST and SECOND
--     order (NULL if they only ordered once). Output: customer, days_to_second.
--     Order by customer.
--
-- HINT: Q1: a CTE with MIN(order_date) per customer, joined to the distinct
-- (month, customer) pairs. Q2: ROW_NUMBER() OVER (PARTITION BY customer ORDER
-- BY order_date) and julianday() differences (or LEAD).
--
-- Expected results for the data below:
--   Q1: 2026-01 2 0 / 2026-02 1 1 / 2026-03 2 2
--   Q2: ana 15 / ben 34 / cy 15 / dee NULL / eli 15

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (customer TEXT NOT NULL, order_date TEXT NOT NULL);
INSERT INTO orders (customer, order_date) VALUES
    ('ana','2026-01-05'),('ana','2026-01-20'),('ana','2026-03-02'),
    ('ben','2026-01-11'),('ben','2026-02-14'),('ben','2026-03-21'),
    ('cy','2026-02-03'),('cy','2026-02-18'),('cy','2026-02-25'),
    ('dee','2026-03-09'),
    ('eli','2026-03-15'),('eli','2026-03-30');

-- Q1
WITH first_order AS (
    SELECT customer, MIN(order_date) AS first_date FROM orders GROUP BY customer
),
monthly AS (
    SELECT DISTINCT substr(order_date, 1, 7) AS month, customer FROM orders
)
SELECT m.month,
       SUM(CASE WHEN substr(f.first_date, 1, 7) = m.month THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN substr(f.first_date, 1, 7) < m.month THEN 1 ELSE 0 END) AS returning_customers
FROM monthly m
JOIN first_order f ON f.customer = m.customer
GROUP BY m.month
ORDER BY m.month;

-- Q2
WITH ranked AS (
    SELECT customer, order_date,
           ROW_NUMBER() OVER (PARTITION BY customer ORDER BY order_date) AS rn
    FROM orders
)
SELECT c.customer,
       CAST(julianday(s.order_date) - julianday(f.order_date) AS INTEGER) AS days_to_second
FROM (SELECT DISTINCT customer FROM orders) c
JOIN ranked f ON f.customer = c.customer AND f.rn = 1
LEFT JOIN ranked s ON s.customer = c.customer AND s.rn = 2
ORDER BY c.customer;

