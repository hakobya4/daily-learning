-- Day 7, Task 1 -- SQL: window frames (moving averages, FIRST_VALUE/LAST_VALUE).
-- Schema: day7-schema.sql (daily_readings_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: For each city, compute a 3-DAY MOVING AVERAGE of temp_c (the
-- current day plus the 2 days before it -- fewer than 3 rows are
-- available yet at the very start of a city's data, which is fine,
-- just average whatever's actually in the window). Order by city,
-- then reading_date. You'll need an explicit window frame:
-- ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.
-- TODO: write this query.


-- Q2: For each row, show the city, reading_date, temp_c, and that
-- city's EARLIEST reading (FIRST_VALUE) and LATEST reading
-- (LAST_VALUE), ordered by reading_date. LAST_VALUE needs an explicit
-- frame too -- by default a window frame only looks back to the
-- current row, so without
-- ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING,
-- LAST_VALUE will just return the current row's own value instead of
-- the city's true latest reading.
-- TODO: write this query.
