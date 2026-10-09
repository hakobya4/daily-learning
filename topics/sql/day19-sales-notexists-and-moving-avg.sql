-- Day 19, Task 1 -- SQL: NOT EXISTS, latest-per-group, moving average, UNION ALL report.
--
-- Self-contained. Load with: sqlite3 practice_day19.db < day19-sales-notexists-and-moving-avg.sql
--
-- THE PROBLEM
-- products(id, name, category) and sales(id, product_id, sold_on, qty, unit_price).
-- Write 5 queries. Nothing is pre-solved.
--
-- Q1: Products never sold in March 2026 (sold_on >= '2026-03-01'), using NOT EXISTS:
--     (name). Order by name.
-- Q2: The most recent sale of each product that has sales:
--     (name, sold_on, qty) using ROW_NUMBER() OVER (PARTITION BY ...). Order by name.
-- Q3: Daily revenue (qty*unit_price) with a 3-row moving average:
--     (sold_on, revenue, moving_avg) where revenue is summed per day, moving_avg
--     is AVG over the current and 2 preceding days (ROWS frame), rounded to 1 decimal.
--     Order by sold_on.
-- Q4: Category report: (category, revenue) for each category, plus a final row
--     ('ALL', total) -- use UNION ALL. Order categories alphabetically, 'ALL' last.
-- Q5: Products whose total qty is above the average total qty of all products
--     that have sales: (name, total_qty). Order by total_qty DESC, name.

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);
CREATE TABLE sales (id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL, sold_on TEXT NOT NULL, qty INTEGER NOT NULL, unit_price INTEGER NOT NULL);

INSERT INTO products (id, name, category) VALUES
 (1,'Pen','office'),(2,'Notebook','office'),(3,'Mug','kitchen'),(4,'Kettle','kitchen'),(5,'Lamp','home');
INSERT INTO sales (id, product_id, sold_on, qty, unit_price) VALUES
 (1,1,'2026-02-27',10,2),(2,2,'2026-02-28',3,6),
 (3,1,'2026-03-01',5,2),(4,3,'2026-03-01',2,9),
 (5,3,'2026-03-02',4,9),(6,2,'2026-03-03',1,6),
 (7,1,'2026-03-03',20,2),(8,4,'2026-02-15',1,30),
 (9,3,'2026-03-05',6,9);

-- Q1:
-- Q2:
-- Q3:
-- Q4:
-- Q5:
