-- Day 25, Task 1 -- SQL: share of total, rank within region, month-over-month.
--
-- Self-contained. Load with: sqlite3 practice_day25.db < day25-region-sales.sql
--
-- THE PROBLEM
-- sales has one row per (region, month) with an amount. Write 3 queries.
-- Nothing pre-solved.
--
-- Q1: For every row: region, month, amount, region_total, pct_of_region
--     (amount / region_total * 100, rounded to 1 decimal).
--     Order by region, month.
-- Q2: The best month per region (highest amount; on a tie take the earlier
--     month): region, month, amount. Order by region.
-- Q3: Month-over-month change per region: region, month, amount,
--     prev_amount, change (amount - prev_amount). The first month of each
--     region has NULL for prev_amount and change. Order by region, month.
--
-- HINT: SUM(amount) OVER (PARTITION BY region) for the total;
-- ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, month) for
-- Q2; LAG(amount) OVER (PARTITION BY region ORDER BY month) for Q3.

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    region TEXT NOT NULL,
    month  TEXT NOT NULL,
    amount INTEGER NOT NULL,
    PRIMARY KEY (region, month)
);
INSERT INTO sales (region, month, amount) VALUES
    ('east', '2026-01', 120), ('east', '2026-02', 150), ('east', '2026-03', 150), ('east', '2026-04', 90),
    ('west', '2026-01', 200), ('west', '2026-02', 180), ('west', '2026-03', 260),
    ('north', '2026-02', 75), ('north', '2026-03', 75), ('north', '2026-04', 110);

-- TODO: write Q1
-- TODO: write Q2
-- TODO: write Q3
