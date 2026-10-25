-- Day 35, Task 1 -- SQL: top spender per month.
--
-- Self-contained. Load with: sqlite3 practice_day35.db < day35-top-spender-per-month.sql
--
-- THE PROBLEM
-- purchases(customer, purchase_date, amount) has one row per purchase;
-- purchase_date is 'YYYY-MM-DD'. Write 3 queries. Nothing pre-solved.
--
-- Q1: Total spent per customer per month. Output: month ('YYYY-MM'),
--     customer, total. Order by month, customer.
-- Q2: The top spender of each month (highest monthly total; on a tie keep
--     the alphabetically first customer). Output: month, customer, total.
--     Order by month.
-- Q3: Customers who were the top spender in at least two different months.
--     Output: customer, months_on_top. Order by customer.
--
-- HINT: strftime('%Y-%m', purchase_date); ROW_NUMBER() OVER (PARTITION BY
-- month ORDER BY total DESC, customer); build on a CTE from Q1.
--
-- Expected results for the data below:
--   Q1: 2026-01 ann 150 / 2026-01 bob 150 / 2026-01 cy 40 /
--       2026-02 ann 30 / 2026-02 bob 200 / 2026-03 ann 90 / 2026-03 cy 90
--   Q2: 2026-01 ann 150 / 2026-02 bob 200 / 2026-03 ann 90
--   Q3: ann 2

CREATE TABLE purchases (customer TEXT, purchase_date TEXT, amount INTEGER);
INSERT INTO purchases VALUES
  ('ann','2026-01-03',100),('ann','2026-01-20',50),
  ('bob','2026-01-10',150),('cy','2026-01-15',40),
  ('ann','2026-02-02',30),('bob','2026-02-11',120),('bob','2026-02-25',80),
  ('ann','2026-03-05',90),('cy','2026-03-09',90);

-- Q1:
SELECT strftime('%Y-%m', purchase_date) AS month, customer, SUM(amount) AS total
FROM purchases
GROUP BY month, customer
ORDER BY month, customer;

-- Q2:
WITH monthly AS (
  SELECT strftime('%Y-%m', purchase_date) AS month, customer, SUM(amount) AS total
  FROM purchases
  GROUP BY month, customer
), ranked AS (
  SELECT month, customer, total,
         ROW_NUMBER() OVER (PARTITION BY month ORDER BY total DESC, customer) AS rn
  FROM monthly
)
SELECT month, customer, total
FROM ranked
WHERE rn = 1
ORDER BY month;

-- Q3:
WITH monthly AS (
  SELECT strftime('%Y-%m', purchase_date) AS month, customer, SUM(amount) AS total
  FROM purchases
  GROUP BY month, customer
), ranked AS (
  SELECT month, customer, total,
         ROW_NUMBER() OVER (PARTITION BY month ORDER BY total DESC, customer) AS rn
  FROM monthly
)
SELECT customer, COUNT(*) AS months_on_top
FROM ranked
WHERE rn = 1
GROUP BY customer
HAVING COUNT(*) >= 2
ORDER BY customer;
