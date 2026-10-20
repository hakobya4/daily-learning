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

-- TODO Q1


-- TODO Q2

