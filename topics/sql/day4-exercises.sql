-- Day 4, Task 1 -- SQL: window functions.
-- Schema: day4-schema.sql (products_sql, sales_sql)
--
-- Q1: For each sale, show the product name, its category, the
-- quantity sold, and that sale's RANK() by quantity WITHIN ITS
-- CATEGORY (highest quantity in the category = rank 1; ties share a
-- rank, per standard RANK() behavior).
-- TODO: write this query (RANK() OVER (PARTITION BY ... ORDER BY ...)).
SELECT P.name AS "product name", P.category, S.quantity AS "quantity sold", RANK() OVER (PARTITION BY P.category ORDER BY S.quantity DESC ) AS "rank"
FROM Sales_Sql S
LEFT OUTER JOIN Products_Sql P
ON S.product_id = P.id;

-- Q2: For each category, list its sales ordered by sale_date, with a
-- RUNNING TOTAL of quantity sold within that category up to and
-- including that sale's date.
SELECT P.category, S.sale_date, S.quantity, SUM(S.quantity) OVER(PARTITION BY P.category ORDER BY S.sale_date) AS "total quantitiy sold"
FROM Products_Sql P
LEFT OUTER JOIN Sales_Sql S
ON P.id = S.product_id;

-- Q3: For each sale, show the quantity and the DIFFERENCE from the
-- PREVIOUS sale's quantity for the SAME PRODUCT, ordered by
-- sale_date. The first sale of a product should show NULL for the
-- difference (there's nothing before it).
SELECT S.product_id, S.sale_date, S.quantity,
    S.quantity - LAG(S.quantity) OVER (PARTITION BY S.product_id ORDER BY S.sale_date) AS "quantity diff"
FROM Sales_Sql S
ORDER BY S.product_id, S.sale_date;


-- Q4: Using ROW_NUMBER() partitioned by category and ordered by
-- quantity descending, list only the TOP 2 highest-quantity sales per
-- category. SQLite has no QUALIFY clause, so you'll need to wrap the
-- ROW_NUMBER() query in an outer SELECT that filters WHERE rn <= 2.
SELECT product_name, category, quantity
FROM (
    SELECT P.name AS product_name, P.category, S.quantity,
        ROW_NUMBER() OVER (PARTITION BY P.category ORDER BY S.quantity DESC) AS rn
    FROM Sales_Sql S
    LEFT OUTER JOIN Products_Sql P
    ON S.product_id = P.id
) ranked
WHERE rn <= 2;
