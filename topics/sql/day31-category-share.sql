-- Day 31, Task 1 -- SQL: category share, top product, above-average products.
--
-- Self-contained. Load with: sqlite3 practice_day31.db < day31-category-share.sql
--
-- THE PROBLEM
-- sales(category, product, amount) holds one row per sale. Write 3 queries.
-- Nothing pre-solved.
--
-- Q1: Revenue per category and its share of the grand total as a percentage
--     rounded to 1 decimal. Output: category, revenue, share_pct.
--     Order by revenue DESC.
-- Q2: The single top-revenue product in each category (no ties in this data).
--     Output: category, product, revenue. Order by category.
-- Q3: Products whose total revenue is STRICTLY greater than the average
--     product revenue of their own category.
--     Output: category, product, revenue. Order by category, product.
--
-- HINT: Q1: SUM(amount) * 100.0 / (SELECT SUM(amount) FROM sales), or
-- SUM(SUM(amount)) OVER (). Q2/Q3: first a CTE with SUM(amount) per
-- (category, product), then ROW_NUMBER() or AVG(revenue) OVER (PARTITION BY
-- category).
--
-- Expected results for the data below:
--   Q1: Books 300 42.9 / Toys 260 37.1 / Games 140 20.0
--   Q2: Books novel 120 / Games chess 90 / Toys robot 200
--   Q3: Books novel 120 / Games chess 90 / Toys robot 200

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (category TEXT NOT NULL, product TEXT NOT NULL, amount INTEGER NOT NULL);
INSERT INTO sales (category, product, amount) VALUES
    ('Books','novel',70),('Books','novel',50),('Books','atlas',80),('Books','cookbook',100),
    ('Toys','robot',120),('Toys','robot',80),('Toys','puzzle',60),
    ('Games','chess',90),('Games','cards',30),('Games','dice',20);

-- Q1
SELECT category,
       SUM(amount) AS revenue,
       ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM sales), 1) AS share_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Q2
WITH prod AS (
    SELECT category, product, SUM(amount) AS revenue
    FROM sales
    GROUP BY category, product
), ranked AS (
    SELECT category, product, revenue,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
    FROM prod
)
SELECT category, product, revenue
FROM ranked
WHERE rn = 1
ORDER BY category;

-- Q3
WITH prod AS (
    SELECT category, product, SUM(amount) AS revenue
    FROM sales
    GROUP BY category, product
), withavg AS (
    SELECT category, product, revenue,
           AVG(revenue) OVER (PARTITION BY category) AS cat_avg
    FROM prod
)
SELECT category, product, revenue
FROM withavg
WHERE revenue > cat_avg
ORDER BY category, product;
