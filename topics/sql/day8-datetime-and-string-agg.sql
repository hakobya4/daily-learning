-- Day 8, Task 1 -- SQL: date/time functions and string aggregation.
-- Schema: day8-schema.sql (deliveries_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: For each region, show the region name and a single
-- comma-and-space-separated string of every driver who delivered
-- there, IN ALPHABETICAL ORDER by driver name (GROUP_CONCAT alone
-- doesn't guarantee row order -- you need an ORDER BY inside the
-- aggregation, e.g. GROUP_CONCAT(driver ORDER BY driver) in SQLite,
-- or an ordered subquery feeding the GROUP_CONCAT if your SQLite
-- build doesn't support ORDER BY inside GROUP_CONCAT).
-- Expected: North -> 'Amara, Ben, Eli, Gus',
--           South -> 'Chen, Dana, Farah, Hana'.
SELECT region, GROUP_CONCAT(driver, ', ') AS drivers
FROM (SELECT region, driver FROM deliveries_sql ORDER BY region, driver)
GROUP BY region
ORDER BY region;


-- Q2: Using STRFTIME('%Y-%m', delivered_at), show each YEAR-MONTH
-- present in the table and how many deliveries happened in it,
-- ordered by year-month ascending.
-- Expected: 2 rows -- '2026-05' -> 1, '2026-06' -> 7.
SELECT STRFTIME('%Y-%m', delivered_at) AS year_month, COUNT(*) AS deliveries
FROM deliveries_sql
GROUP BY year_month
ORDER BY year_month;


-- Q3: Using DATE() arithmetic (DATE('2026-06-15', '-7 days') gives you
-- the date 7 days before a reference date), show the driver, region,
-- and delivered_at for every delivery that happened WITHIN THE LAST 7
-- DAYS of '2026-06-15' (inclusive of both ends of that 7-day window),
-- ordered by delivered_at.
-- Expected: 4 rows, in delivered_at order -- Dana/South/06-10,
--           Eli/North/06-12, Hana/South/06-14, Gus/North/06-15.
SELECT driver, region, delivered_at
FROM deliveries_sql
WHERE delivered_at BETWEEN DATE('2026-06-15', '-7 days') AND '2026-06-15'
ORDER BY delivered_at;
