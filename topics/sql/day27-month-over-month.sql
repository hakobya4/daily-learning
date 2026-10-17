-- Day 27, Task 1 -- SQL: LAG/LEAD, month-over-month change, running totals.
--
-- Self-contained. Load with: sqlite3 practice_day27.db < day27-month-over-month.sql
--
-- THE PROBLEM
-- monthly_revenue has one row per (product, month). Write 3 queries.
-- Nothing pre-solved.
--
-- Q1: For every row: product, month, revenue, prev_revenue (previous month
--     of the SAME product, NULL for the first) and pct_change
--     (ROUND((revenue-prev)*100.0/prev, 1), NULL when there is no prev).
--     Order by product, month.
-- Q2: Running total per product: product, month, revenue, running_total.
--     Order by product, month.
-- Q3: Products whose revenue DROPPED in two consecutive months at least
--     once (rev < previous AND previous < the one before). Output
--     product only, one row each, ordered by product.
--
-- HINT: LAG(revenue, 1) OVER (PARTITION BY product ORDER BY month);
-- running totals use SUM(...) OVER (PARTITION BY ... ORDER BY ...).

DROP TABLE IF EXISTS monthly_revenue;
CREATE TABLE monthly_revenue (
    product TEXT NOT NULL,
    month   TEXT NOT NULL,   -- 'YYYY-MM'
    revenue INTEGER NOT NULL,
    PRIMARY KEY (product, month)
);
INSERT INTO monthly_revenue (product, month, revenue) VALUES
    ('widget', '2026-01', 100), ('widget', '2026-02', 120), ('widget', '2026-03', 90),
    ('widget', '2026-04', 80),  ('widget', '2026-05', 95),
    ('gadget', '2026-01', 50),  ('gadget', '2026-02', 55),  ('gadget', '2026-03', 60),
    ('gizmo',  '2026-02', 200), ('gizmo',  '2026-03', 150), ('gizmo',  '2026-04', 100);

-- Q1: month-over-month change
SELECT product, month, revenue, prev_revenue,
       ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 1) AS pct_change
FROM (
    SELECT product, month, revenue,
           LAG(revenue, 1) OVER (PARTITION BY product ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
ORDER BY product, month;

-- Q2: running total per product
SELECT product, month, revenue,
       SUM(revenue) OVER (PARTITION BY product ORDER BY month) AS running_total
FROM monthly_revenue
ORDER BY product, month;

-- Q3: products with two consecutive drops at least once
SELECT DISTINCT product
FROM (
    SELECT product, revenue,
           LAG(revenue, 1) OVER (PARTITION BY product ORDER BY month) AS p1,
           LAG(revenue, 2) OVER (PARTITION BY product ORDER BY month) AS p2
    FROM monthly_revenue
)
WHERE revenue < p1 AND p1 < p2
ORDER BY product;
