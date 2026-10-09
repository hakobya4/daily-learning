-- Day 18, Task 1 -- SQL: anti-join, LAG month-over-month, share of total, FIRST/LAST_VALUE, HAVING.
--
-- Self-contained. Load with: sqlite3 practice_day18.db < day18-orders-lag-and-first-last.sql
--
-- THE PROBLEM
-- customers(id, name, country) and orders(id, customer_id, ordered_on, amount, status).
-- Write 5 queries. Nothing is pre-solved.
--
-- Q1: Customers with no orders at all: (name). Order by name.
-- Q2: Monthly paid totals with month-over-month change:
--     (month, total, prev_total, change) where month = strftime('%Y-%m', ordered_on),
--     only status = 'paid', prev_total/change are NULL for the first month
--     (use LAG). Order by month.
-- Q3: Each paid order's share of its customer's paid total:
--     (id, customer_id, pct) with pct rounded to 1 decimal. Order by id.
-- Q4: For each customer with paid orders, first and latest paid order amount:
--     (name, first_amount, last_amount) (FIRST_VALUE / LAST_VALUE with a full
--     frame, or other technique). Order by name.
-- Q5: Countries whose average paid order is above 100 AND with at least 2 paid
--     orders: (country, orders, avg_amount) avg rounded to 2 decimals. Order by country.

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, ordered_on TEXT NOT NULL, amount INTEGER NOT NULL, status TEXT NOT NULL);

INSERT INTO customers (id, name, country) VALUES
 (1,'Anya','CA'),(2,'Boris','US'),(3,'Chen','US'),(4,'Dara','CA'),(5,'Eli','DE');
INSERT INTO orders (id, customer_id, ordered_on, amount, status) VALUES
 (1,1,'2026-01-05',100,'paid'),(2,1,'2026-02-10',250,'paid'),
 (3,2,'2026-01-20',80,'paid'),(4,2,'2026-02-02',40,'refunded'),
 (5,3,'2026-02-14',300,'paid'),(6,3,'2026-03-01',60,'paid'),
 (7,1,'2026-03-15',50,'paid'),(8,2,'2026-03-20',120,'paid'),
 (9,4,'2026-03-22',500,'pending');

-- Q1:
SELECT c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL
ORDER BY c.name;

-- Q2:
WITH monthly AS (
  SELECT strftime('%Y-%m', ordered_on) AS month, SUM(amount) AS total
  FROM orders
  WHERE status = 'paid'
  GROUP BY month
)
SELECT month,
       total,
       LAG(total) OVER (ORDER BY month) AS prev_total,
       total - LAG(total) OVER (ORDER BY month) AS change
FROM monthly
ORDER BY month;

-- Q3:
SELECT id,
       customer_id,
       ROUND(100.0 * amount / SUM(amount) OVER (PARTITION BY customer_id), 1) AS pct
FROM orders
WHERE status = 'paid'
ORDER BY id;

-- Q4:
SELECT DISTINCT c.name,
       FIRST_VALUE(o.amount) OVER w AS first_amount,
       LAST_VALUE(o.amount) OVER w AS last_amount
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'paid'
WINDOW w AS (PARTITION BY o.customer_id ORDER BY o.ordered_on, o.id
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY c.name;

-- Q5:
SELECT c.country,
       COUNT(*) AS orders,
       ROUND(AVG(o.amount), 2) AS avg_amount
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'paid'
GROUP BY c.country
HAVING COUNT(*) >= 2 AND AVG(o.amount) > 100
ORDER BY c.country;
