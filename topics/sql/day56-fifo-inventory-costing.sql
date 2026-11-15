-- Day 56, Task 3 -- SQL: FIFO inventory costing with cumulative-quantity ranges.
--
-- Self-contained. Load with: sqlite3 practice_day56.db < day56-fifo-inventory-costing.sql
-- (needs window functions: SQLite >= 3.25, or any PostgreSQL / MySQL 8).
--
-- THE PROBLEM
-- purchases(lot_id, item, purchased_on, qty, unit_cost) -- stock arriving in lots.
-- sales(sale_id, item, sold_on, qty, unit_price).
-- Sales consume stock FIFO per item: lots in (purchased_on, lot_id) order are used up by
-- sales in (sold_on, sale_id) order, a sale may span several lots, and a lot may feed
-- several sales. (Treat it purely as a queue -- ignore whether the lot had arrived by the
-- sale date.) If an item runs out, the rest of that sale is UNFILLED.
-- Write 4 queries below the data. No procedural loops / recursive CTEs needed. Nothing
-- pre-solved.
--
-- Q1: The FIFO allocation: one row per (sale, lot) pair that actually exchanged units.
--     Output: sale_id, lot_id, qty_allocated. Order by sale_id, lot_id.
--     Hint: give every lot a half-open range of "unit numbers" [lo, hi) on its item's
--     running total -- hi = SUM(qty) OVER (PARTITION BY item ORDER BY purchased_on, lot_id),
--     lo = hi - qty -- and do the same for sales. A sale and a lot of the same item
--     overlap iff s.lo < l.hi AND l.lo < s.hi, and the overlap size is
--     MIN(s.hi, l.hi) - MAX(s.lo, l.lo) (SQLite's 2-arg MIN/MAX are scalar;
--     PostgreSQL uses LEAST/GREATEST).
-- Q2: Per sale: sale_id, item, filled_qty, unfilled_qty, revenue, cogs, profit, where
--     revenue = filled_qty * unit_price (unfilled units are not billed),
--     cogs = SUM(qty_allocated * lot unit_cost), profit = revenue - cogs.
--     Every sale appears. Order by sale_id.
-- Q3: Stock still on hand after all sales: item, lot_id, purchased_on, remaining_qty,
--     only lots with remaining_qty > 0 (including lots of items never sold, and lots that
--     were only PARTLY consumed). Order by item, lot_id.
-- Q4: Items whose sales exceed everything ever purchased:
--     item, total_sold, total_purchased, shortfall. Order by item.
--
-- Expected results for the data below:
--   Q1: 101|1|7   102|1|3   102|2|3   103|3|3   104|2|2   104|4|2
--       105|3|5   105|5|4   106|6|3
--   Q2: 101|bolt|7|0|35|14|21    102|bolt|6|0|36|15|21    103|nut|3|0|9|3|6
--       104|bolt|4|0|24|14|10    105|nut|9|0|27|13|14     106|gear|3|2|45|30|15
--   Q3: bolt|4|2026-11-08|8   nut|7|2026-11-12|6   washer|8|2026-11-02|20
--   Q4: gear|5|3|2

CREATE TABLE purchases (lot_id INTEGER PRIMARY KEY, item TEXT, purchased_on TEXT,
                        qty INTEGER, unit_cost INTEGER);
INSERT INTO purchases VALUES
 (1, 'bolt', '2026-11-01', 10, 2),
 (2, 'bolt', '2026-11-03',  5, 3),
 (3, 'nut',  '2026-11-02',  8, 1),
 (4, 'bolt', '2026-11-08', 10, 4),
 (5, 'nut',  '2026-11-09',  4, 2),
 (6, 'gear', '2026-11-05',  3, 10),
 (7, 'nut',  '2026-11-12',  6, 2),
 (8, 'washer', '2026-11-02', 20, 1);

CREATE TABLE sales (sale_id INTEGER PRIMARY KEY, item TEXT, sold_on TEXT,
                    qty INTEGER, unit_price INTEGER);
INSERT INTO sales VALUES
 (101, 'bolt', '2026-11-04',  7, 5),
 (102, 'bolt', '2026-11-06',  6, 6),
 (103, 'nut',  '2026-11-07',  3, 3),
 (104, 'bolt', '2026-11-10',  4, 6),
 (105, 'nut',  '2026-11-10',  9, 3),
 (106, 'gear', '2026-11-11',  5, 15);

-- Q1
-- TODO: your query here

-- Q2
-- TODO: your query here

-- Q3
-- TODO: your query here

-- Q4
-- TODO: your query here
