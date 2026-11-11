-- Day 51, Task 6 -- SQL: returns, anti-join and net revenue.
--
-- Self-contained. Load with: sqlite3 practice_day51.db < day51-orders-returns.sql
--
-- THE PROBLEM
-- orders(id, customer, order_date, amount); returns(order_id, return_date, refund) -- a
-- return refunds all or part of one order. Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Number of returned orders per customer (only customers with at least one return).
--     Output: customer, returned_orders. Order by returned_orders DESC, customer.
-- Q2: Orders that were never returned. Output: id. Order by id.   Hint: NOT EXISTS / LEFT JOIN ... IS NULL.
-- Q3: Net revenue per customer = sum(amount) minus sum(refund), counting customers with no
--     returns too. Output: customer, net. Order by net DESC, customer.   Hint: LEFT JOIN + COALESCE.
-- Q4: Per order month (YYYY-MM): gross revenue and net revenue (refunds are attributed to the
--     month of the ORDER, not of the return). Output: month, gross, net. Order by month.
--
-- Expected results for the data below:
--   Q1: ann|2  bob|1  cat|1
--   Q2: 1  3  5  7
--   Q3: ann|120  bob|75  cat|40  dan|20
--   Q4: 2026-01|150|80  2026-02|190|85  2026-03|100|90

CREATE TABLE orders (id INTEGER, customer TEXT, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'ann','2026-01-05',50),
 (2,'ann','2026-01-20',70),
 (3,'bob','2026-01-11',30),
 (4,'bob','2026-02-02',90),
 (5,'cat','2026-02-14',40),
 (6,'cat','2026-02-15',60),
 (7,'dan','2026-03-01',20),
 (8,'ann','2026-03-09',80);
CREATE TABLE returns (order_id INTEGER, return_date TEXT, refund INTEGER);
INSERT INTO returns VALUES
 (2,'2026-01-25',70),
 (4,'2026-02-10',45),
 (6,'2026-02-20',60),
 (8,'2026-03-12',10);

-- Q1
SELECT o.customer, COUNT(DISTINCT o.id) AS returned_orders
FROM orders o JOIN returns r ON r.order_id = o.id
GROUP BY o.customer
ORDER BY returned_orders DESC, o.customer;

-- Q2
SELECT o.id
FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM returns r WHERE r.order_id = o.id)
ORDER BY o.id;

-- Q3
SELECT o.customer, SUM(o.amount) - COALESCE(SUM(r.refund), 0) AS net
FROM orders o
LEFT JOIN (SELECT order_id, SUM(refund) AS refund FROM returns GROUP BY order_id) r
  ON r.order_id = o.id
GROUP BY o.customer
ORDER BY net DESC, o.customer;

-- Q4
SELECT substr(o.order_date, 1, 7) AS month,
       SUM(o.amount) AS gross,
       SUM(o.amount) - COALESCE(SUM(r.refund), 0) AS net
FROM orders o
LEFT JOIN (SELECT order_id, SUM(refund) AS refund FROM returns GROUP BY order_id) r
  ON r.order_id = o.id
GROUP BY month
ORDER BY month;
