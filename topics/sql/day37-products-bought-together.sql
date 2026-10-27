-- Day 37, Task 1 -- SQL: products bought together.
--
-- Self-contained. Load with: sqlite3 practice_day37.db < day37-products-bought-together.sql
--
-- THE PROBLEM
-- order_items(order_id, product). Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: All product PAIRS (a, b) with a < b that appear together in the same
--     order, with the number of orders containing both (pair_count).
--     Output: a, b, pair_count. Order by pair_count DESC, a, b.
-- Q2: Only pairs bought together in at least 2 orders. Same columns/order.
-- Q3: Products that never appear in an order with any other product
--     (the only item in all their orders). Output: product. Order by product.
--
-- HINT: self-join order_items on order_id with a.product < b.product, then
-- GROUP BY; Q3 can use NOT EXISTS or GROUP BY order_id HAVING COUNT(*) = 1.
--
-- Expected results for the data below:
--   Q1: bread|milk|3, bread|butter|1, bread|eggs|1, butter|milk|1, eggs|milk|1
--   Q2: bread|milk|3
--   Q3: tea

CREATE TABLE order_items (order_id INTEGER, product TEXT);
INSERT INTO order_items VALUES
  (1,'bread'),(1,'milk'),(1,'butter'),
  (2,'bread'),(2,'milk'),
  (3,'bread'),(3,'milk'),(3,'eggs'),
  (4,'tea'),
  (5,'tea');

-- Q1
SELECT a.product AS a, b.product AS b, COUNT(*) AS pair_count
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product < b.product
GROUP BY a.product, b.product
ORDER BY pair_count DESC, a, b;

-- Q2
SELECT a.product AS a, b.product AS b, COUNT(*) AS pair_count
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product < b.product
GROUP BY a.product, b.product
HAVING COUNT(*) >= 2
ORDER BY pair_count DESC, a, b;

-- Q3
SELECT DISTINCT product
FROM order_items o
WHERE NOT EXISTS (
  SELECT 1 FROM order_items x
  WHERE x.order_id = o.order_id AND x.product <> o.product
)
AND NOT EXISTS (
  SELECT 1 FROM order_items y
  WHERE y.product = o.product
    AND EXISTS (SELECT 1 FROM order_items z
                WHERE z.order_id = y.order_id AND z.product <> y.product)
)
ORDER BY product;

