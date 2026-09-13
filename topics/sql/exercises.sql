-- Day 2 -- SQL exercises: joins, aggregation, and NULL handling.

-- Q1: List the name of every customer who lives in 'Toronto'.
SELECT c.name 
FROM customers_sql AS c 
WHERE c.city = 'Toronto';


-- Q2: For each customer who has placed at least one order, show their
-- name and their TOTAL amount spent, highest spender first. Customers
-- with zero orders should NOT appear.
SELECT c.name, SUM(o.amount) as order_amount
FROM customers_sql AS c
INNER JOIN orders_sql AS o
ON c.id = o.customer_id
GROUP BY c.name
ORDER BY order_amount DESC;


-- Q3: List every customer who has NEVER placed an order.

SELECT c.name 
FROM customers_sql AS c
LEFT JOIN orders_sql AS o
ON c.id = o.customer_id
WHERE o.amount IS NULL;


-- Q4: For each customer who has ordered, show their name and the date
-- of their MOST RECENT order.
-- Expected: 4 rows -- Alice 2026-05-01, Bob 2026-02-20,
--           Carol 2026-01-15, Dave 2026-04-01.
-- Hint: MAX(order_date) grouped by customer works here because the
-- dates are in 'YYYY-MM-DD' format, which sorts correctly as text.
-- TODO: write this query.
SELECT c.name, MAX(o.order_date)
FROM customers_sql AS c
INNER JOIN orders_sql AS o
ON c.id = o.customer_id
GROUP BY c.name; 

-- Q5: List customers whose TOTAL spending is above the AVERAGE total
-- spending across all customers who have ordered.

SELECT 
    c.name, 
    SUM(o.amount) AS total_spent
FROM customers_sql AS c
INNER JOIN orders_sql AS o ON c.id = o.customer_id
GROUP BY c.name
HAVING SUM(o.amount) > (
    SELECT AVG(customer_total)
    FROM (
        SELECT SUM(amount) AS customer_total
        FROM orders_sql
        GROUP BY customer_id
    ) AS subquery
);