-- Day 45, Task 6 -- SQL: consecutive months, running share, first/last per group.
--
-- Self-contained. Load with: sqlite3 practice_day45.db < day45-consecutive-months.sql
--
-- THE PROBLEM
-- orders(id, customer, order_month TEXT 'YYYY-MM', amount). Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Customers who ordered in at least 3 CONSECUTIVE months (months with
--     several orders count once). Output: customer. Order by customer.
--     Hint: distinct (customer, month), month index = year*12+month,
--     index - ROW_NUMBER() OVER (PARTITION BY customer ORDER BY idx) is constant in a run.
-- Q2: For every order: customer, order_month, amount, and the customer's running
--     total up to and including that row (order by order_month, id).
--     Output ordered by customer, order_month, id.
-- Q3: Per customer: the amount of their FIRST order and of their LAST order
--     (by order_month, id). Output: customer, first_amount, last_amount. Order by customer.
--
-- Expected results for the data below:
--   Q1: ann
--   Q2: ann|2026-01|100|100  ann|2026-02|50|150  ann|2026-02|25|175  ann|2026-03|75|250
--       bob|2026-01|10|10  bob|2026-03|20|30  bob|2026-04|30|60
--       cy|2026-05|500|500
--   Q3: ann|100|75  bob|10|30  cy|500|500

CREATE TABLE orders (id INTEGER, customer TEXT, order_month TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'ann','2026-01',100),(2,'ann','2026-02',50),(3,'ann','2026-02',25),
 (4,'ann','2026-03',75),(5,'bob','2026-01',10),(6,'bob','2026-03',20),
 (7,'bob','2026-04',30),(8,'cy','2026-05',500);

-- Q1
WITH m AS (
  SELECT DISTINCT customer, order_month,
         CAST(substr(order_month,1,4) AS INTEGER)*12 + CAST(substr(order_month,6,2) AS INTEGER) AS idx
  FROM orders
),
g AS (
  SELECT customer, idx - ROW_NUMBER() OVER (PARTITION BY customer ORDER BY idx) AS grp
  FROM m
)
SELECT DISTINCT customer FROM g GROUP BY customer, grp HAVING COUNT(*) >= 3
ORDER BY customer;

-- Q2
SELECT customer, order_month, amount,
       SUM(amount) OVER (PARTITION BY customer ORDER BY order_month, id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
ORDER BY customer, order_month, id;

-- Q3
WITH r AS (
  SELECT customer, amount,
         ROW_NUMBER() OVER (PARTITION BY customer ORDER BY order_month, id) AS rn_asc,
         ROW_NUMBER() OVER (PARTITION BY customer ORDER BY order_month DESC, id DESC) AS rn_desc
  FROM orders
)
SELECT customer,
       MAX(CASE WHEN rn_asc = 1 THEN amount END) AS first_amount,
       MAX(CASE WHEN rn_desc = 1 THEN amount END) AS last_amount
FROM r GROUP BY customer ORDER BY customer;
