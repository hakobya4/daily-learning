-- Day 6, Task 2 -- SQL: conditional aggregation (CASE WHEN + pivoting).
--
-- Self-contained: schema + data + queries all in this one file.
-- Load it with: sqlite3 practice_day6b.db < day6-conditional-aggregation.sql
--
-- Nothing below is pre-solved. Write each query yourself.

DROP TABLE IF EXISTS sales_by_quarter_sql;

CREATE TABLE sales_by_quarter_sql (
    id      INTEGER PRIMARY KEY,
    region  TEXT NOT NULL,
    quarter TEXT NOT NULL,   -- 'Q1'..'Q4'
    amount  REAL NOT NULL
);

INSERT INTO sales_by_quarter_sql (id, region, quarter, amount) VALUES
    (1,  'North', 'Q1', 120),
    (2,  'North', 'Q2', 80),
    (3,  'North', 'Q3', 200),
    (4,  'North', 'Q4', 60),
    (5,  'South', 'Q1', 300),
    (6,  'South', 'Q2', 40),
    (7,  'South', 'Q3', 90),
    (8,  'South', 'Q4', 250),
    (9,  'East',  'Q1', 30),
    (10, 'East',  'Q4', 400);
-- note: East has no Q2 or Q3 rows at all -- deliberate, so the pivot
-- query needs to produce a 0 (not NULL, not a missing row) for those
-- cells.

-- Q1: PIVOT this into one row per region, with four columns
-- (total_q1, total_q2, total_q3, total_q4) holding that region's
-- summed amount for each quarter -- 0 where a region has no rows for
-- a given quarter. Use SUM(CASE WHEN quarter = '...' THEN amount ELSE 0 END)
-- for each column, GROUP BY region.
SELECT
    region,
    SUM(CASE WHEN quarter = 'Q1' THEN amount ELSE 0 END) AS total_q1,
    SUM(CASE WHEN quarter = 'Q2' THEN amount ELSE 0 END) AS total_q2,
    SUM(CASE WHEN quarter = 'Q3' THEN amount ELSE 0 END) AS total_q3,
    SUM(CASE WHEN quarter = 'Q4' THEN amount ELSE 0 END) AS total_q4
FROM sales_by_quarter_sql
GROUP BY region
ORDER BY region;


-- Q2: Without aggregating, label EVERY individual sale as 'low'
-- (amount < 100), 'medium' (100-249), or 'high' (250+) in a new
-- column called `size_bucket`, alongside its region and amount. Use a
-- single CASE WHEN expression (not three separate queries).
SELECT
    region,
    amount,
    CASE
        WHEN amount < 100 THEN 'low'
        WHEN amount < 250 THEN 'medium'
        ELSE 'high'
    END AS size_bucket
FROM sales_by_quarter_sql
ORDER BY id;


-- Q3: Using conditional aggregation again, show each region alongside
-- a COUNT of how many of its sales are 'high' (250+) by the same
-- thresholds as Q2 -- regions with zero high sales should show 0, not
-- be omitted. (COUNT(CASE WHEN ... THEN 1 END) is the pattern here --
-- COUNT ignores NULLs, so only matching rows get counted.)
SELECT
    region,
    COUNT(CASE WHEN amount >= 250 THEN 1 END) AS high_sales_count
FROM sales_by_quarter_sql
GROUP BY region
ORDER BY region;
