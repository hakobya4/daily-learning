-- Day 46, Task 6 -- SQL: anti-join, top-N per group, share of total.
--
-- Self-contained. Load with: sqlite3 practice_day46.db < day46-product-revenue.sql
--
-- THE PROBLEM
-- products(id, name, category), order_items(order_id, product_id, qty, unit_price).
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Products that were NEVER ordered (anti-join). Output: name. Order by name.
-- Q2: Top 2 products by revenue (SUM(qty*unit_price)) within each category,
--     ties broken by name. Output: category, name, revenue. Order by category, revenue DESC, name.
--     Hint: aggregate in a CTE, then ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC, name).
-- Q3: Each category's share of total revenue as a percentage rounded to 1 decimal.
--     Output: category, revenue, pct. Order by revenue DESC.
--     Hint: SUM(revenue) OVER () for the grand total; multiply by 100.0.
--
-- Expected results for the data below:
--   Q1: cable|stand
--   Q2: audio|buds|300  audio|speaker|200
--       misc|lamp|300
--       office|desk|500  office|chair|400
--   Q3: office|900|52.9  audio|500|29.4  misc|300|17.6

CREATE TABLE products (id INTEGER, name TEXT, category TEXT);
INSERT INTO products VALUES
 (1,'buds','audio'),(2,'speaker','audio'),(3,'desk','office'),(4,'chair','office'),
 (5,'stand','office'),(6,'cable','audio'),(7,'lamp','misc');
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price INTEGER);
INSERT INTO order_items VALUES
 (1,1,2,100),(1,2,1,200),(2,1,1,100),(2,3,1,500),(3,4,2,200),(3,7,3,100);

-- Q1

-- Q2

-- Q3
