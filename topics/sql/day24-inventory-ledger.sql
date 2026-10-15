-- Day 24, Task 1 -- SQL: inventory ledger, running stock and stock-outs.
--
-- Self-contained. Load with: sqlite3 practice_day24.db < day24-inventory-ledger.sql
--
-- THE PROBLEM
-- stock_moves has one row per stock movement: qty > 0 is stock received,
-- qty < 0 is stock shipped out. Moves are ordered by (move_date, id).
-- Write 3 queries. Nothing pre-solved.
--
-- Q1: Running balance per sku after every move:
--     id, sku, move_date, qty, balance. Order by sku, move_date, id.
-- Q2: Moves that pushed a sku's balance below zero (the first such move
--     per sku only): sku, id, balance. Order by sku.
-- Q3: Final balance per sku plus the date of its LAST receipt (qty > 0):
--     sku, final_balance, last_receipt_date. Order by sku.
--
-- HINT: SUM(qty) OVER (PARTITION BY sku ORDER BY move_date, id) gives the
-- running balance. For Q2 wrap Q1 in a CTE and keep the row with
-- MIN(id) among rows where balance < 0 (or use ROW_NUMBER()).

DROP TABLE IF EXISTS stock_moves;
CREATE TABLE stock_moves (
    id        INTEGER PRIMARY KEY,
    sku       TEXT NOT NULL,
    move_date TEXT NOT NULL,
    qty       INTEGER NOT NULL
);
INSERT INTO stock_moves (id, sku, move_date, qty) VALUES
    (1,  'apple',  '2026-10-01',  100),
    (2,  'apple',  '2026-10-02',  -30),
    (3,  'apple',  '2026-10-03',  -80),
    (4,  'apple',  '2026-10-04',   50),
    (5,  'apple',  '2026-10-05',  -40),
    (6,  'pear',   '2026-10-01',   20),
    (7,  'pear',   '2026-10-02',  -20),
    (8,  'pear',   '2026-10-03',   10),
    (9,  'plum',   '2026-10-02',  -5),
    (10, 'plum',   '2026-10-03',   30),
    (11, 'plum',   '2026-10-03',  -10),
    (12, 'plum',   '2026-10-06',  -30);

-- Q1:
SELECT id, sku, move_date, qty,
       SUM(qty) OVER (PARTITION BY sku ORDER BY move_date, id) AS balance
FROM stock_moves
ORDER BY sku, move_date, id;

-- Q2:
WITH running AS (
    SELECT id, sku, move_date, qty,
           SUM(qty) OVER (PARTITION BY sku ORDER BY move_date, id) AS balance
    FROM stock_moves
), negative AS (
    SELECT sku, id, balance,
           ROW_NUMBER() OVER (PARTITION BY sku ORDER BY move_date, id) AS rn
    FROM running
    WHERE balance < 0
)
SELECT sku, id, balance
FROM negative
WHERE rn = 1
ORDER BY sku;

-- Q3:
SELECT sku,
       SUM(qty) AS final_balance,
       MAX(CASE WHEN qty > 0 THEN move_date END) AS last_receipt_date
FROM stock_moves
GROUP BY sku
ORDER BY sku;
