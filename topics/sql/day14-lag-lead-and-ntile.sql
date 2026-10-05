-- Day 14, Task 1 -- SQL: LAG/LEAD, FIRST_VALUE, NTILE and share-of-total.
--
-- Self-contained. Load with: sqlite3 practice_day14.db < day14-lag-lead-and-ntile.sql
--
-- THE PROBLEM
-- monthly_sales(id, region, month, revenue) where month is 'YYYY-MM'.
-- Write 5 queries. Nothing is pre-solved.
--
-- Q1: Month-over-month change per region: (region, month, revenue,
--     prev_revenue, change) using LAG(revenue) OVER (PARTITION BY region
--     ORDER BY month). The first month of a region has NULL prev/change.
--     Order by region, month.
-- Q2: Months where revenue DROPPED versus the previous month in the same
--     region (region, month, change). Hint: wrap Q1 in a CTE.
-- Q3: For each row also show the region's best-ever month's revenue and
--     how far this month is below it: (region, month, revenue, best,
--     gap_to_best). Use MAX(...) OVER (PARTITION BY region) or
--     FIRST_VALUE(revenue) OVER (... ORDER BY revenue DESC).
-- Q4: Share of total: each row's percent of its MONTH's total revenue
--     across regions, rounded to 1 decimal (region, month, pct).
--     Order by month, region.
-- Q5: NTILE(2) over all rows ordered by revenue DESC -> (region, month,
--     revenue, half) where half is 1 (top) or 2 (bottom).
--     Order by half, revenue DESC, region.

DROP TABLE IF EXISTS monthly_sales;
CREATE TABLE monthly_sales (
    id      INTEGER PRIMARY KEY,
    region  TEXT NOT NULL,
    month   TEXT NOT NULL,
    revenue INTEGER NOT NULL
);
INSERT INTO monthly_sales (id, region, month, revenue) VALUES
    (1,  'east', '2026-01', 100),
    (2,  'east', '2026-02', 120),
    (3,  'east', '2026-03',  90),
    (4,  'east', '2026-04', 150),
    (5,  'west', '2026-01',  80),
    (6,  'west', '2026-02',  80),
    (7,  'west', '2026-03', 110),
    (8,  'west', '2026-04',  70),
    (9,  'north','2026-01',  60),
    (10, 'north','2026-02',  75),
    (11, 'north','2026-03',  65),
    (12, 'north','2026-04',  95);

-- Q1:
SELECT region, month, revenue,
       LAG(revenue) OVER (PARTITION BY region ORDER BY month) AS prev_revenue,
       revenue - LAG(revenue) OVER (PARTITION BY region ORDER BY month) AS change
FROM monthly_sales
ORDER BY region, month;

-- Q2:
WITH mom AS (
    SELECT region, month,
           revenue - LAG(revenue) OVER (PARTITION BY region ORDER BY month) AS change
    FROM monthly_sales
)
SELECT region, month, change
FROM mom
WHERE change < 0
ORDER BY region, month;

-- Q3:
SELECT region, month, revenue,
       MAX(revenue) OVER (PARTITION BY region) AS best,
       MAX(revenue) OVER (PARTITION BY region) - revenue AS gap_to_best
FROM monthly_sales
ORDER BY region, month;

-- Q4:
SELECT region, month,
       ROUND(100.0 * revenue / SUM(revenue) OVER (PARTITION BY month), 1) AS pct
FROM monthly_sales
ORDER BY month, region;

-- Q5:
SELECT region, month, revenue, half
FROM (
    SELECT region, month, revenue,
           NTILE(2) OVER (ORDER BY revenue DESC) AS half
    FROM monthly_sales
)
ORDER BY half, revenue DESC, region;
