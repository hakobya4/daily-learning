-- Day 4, Task 1 -- SQL: window functions.
-- Schema: day4-schema.sql (products_sql, sales_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: For each sale, show the product name, its category, the
-- quantity sold, and that sale's RANK() by quantity WITHIN ITS
-- CATEGORY (highest quantity in the category = rank 1; ties share a
-- rank, per standard RANK() behavior).
-- TODO: write this query (RANK() OVER (PARTITION BY ... ORDER BY ...)).


-- Q2: For each category, list its sales ordered by sale_date, with a
-- RUNNING TOTAL of quantity sold within that category up to and
-- including that sale's date.
-- TODO: write this query (SUM() OVER (PARTITION BY ... ORDER BY ...)).


-- Q3: For each sale, show the quantity and the DIFFERENCE from the
-- PREVIOUS sale's quantity for the SAME PRODUCT, ordered by
-- sale_date. The first sale of a product should show NULL for the
-- difference (there's nothing before it).
-- TODO: write this query (LAG() OVER (PARTITION BY product_id ORDER BY sale_date)).


-- Q4: Using ROW_NUMBER() partitioned by category and ordered by
-- quantity descending, list only the TOP 2 highest-quantity sales per
-- category. SQLite has no QUALIFY clause, so you'll need to wrap the
-- ROW_NUMBER() query in an outer SELECT that filters WHERE rn <= 2.
-- TODO: write this query.
