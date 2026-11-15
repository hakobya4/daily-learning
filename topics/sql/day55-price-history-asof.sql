-- Day 55, Task 6 -- SQL: as-of joins against a price history (slowly changing prices).
--
-- Self-contained. Load with: sqlite3 practice_day55.db < day55-price-history-asof.sql
-- (needs window functions: SQLite >= 3.25, or any PostgreSQL / MySQL 8).
--
-- THE PROBLEM
-- price_history(product, valid_from, price) -- a product's price is `price` from
--   valid_from (inclusive) until the next valid_from for the same product (exclusive).
--   Before its first valid_from a product has NO price.
-- orders(id, product, order_date, qty).
-- Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: The unit price in effect for every order ("as-of" lookup) and the line total.
--     Orders placed before the product's first price get NULL price and NULL total.
--     Output: id, product, order_date, unit_price, line_total. Order by id.
--     Hint: either a correlated subquery picking the row with the greatest
--     valid_from <= order_date, or first turn price_history into ranges with
--     LEAD(valid_from) OVER (PARTITION BY product ORDER BY valid_from) AS valid_to and
--     LEFT JOIN on order_date >= valid_from AND (valid_to IS NULL OR order_date < valid_to).
-- Q2: Revenue per product (sum of line totals, ignoring unpriced orders; products with no
--     priced orders show 0). Include every product that appears in price_history OR
--     orders. Output: product, revenue. Order by revenue DESC, product.
-- Q3: Every price change that was an increase of MORE than 10% over the previous price for
--     the same product. Output: product, valid_from, old_price, new_price, pct_increase
--     where pct_increase = ROUND(100.0 * (new - old) / old, 1).
--     Order by product, valid_from.
-- Q4: For each product, the number of DAYS each price was in effect, up to and including
--     the reporting date 2026-11-30 for the current (open-ended) price.
--     A price from 2026-11-01 replaced on 2026-11-10 was in effect 9 days.
--     The open-ended price from 2026-11-25 counts 2026-11-25..2026-11-30 = 6 days.
--     Output: product, valid_from, price, days_in_effect. Order by product, valid_from.
--     Hint: JULIANDAY(x) - JULIANDAY(y) in SQLite (date subtraction in PostgreSQL);
--     COALESCE the LEAD() with DATE('2026-11-30', '+1 day').
--
-- Expected results for the data below:
--   Q1: 1|apple|2026-10-30|NULL|NULL       2|apple|2026-11-01|10|30
--       3|apple|2026-11-09|10|20           4|apple|2026-11-10|12|12
--       5|apple|2026-11-28|15|60           6|pear|2026-11-05|20|100
--       7|pear|2026-11-20|18|36            8|plum|2026-11-15|5|5
--       9|apple|2026-11-24|12|24
--   Q2: apple|146   pear|136   plum|5   kiwi|0
--   Q3: apple|2026-11-10|10|12|20.0   apple|2026-11-25|12|15|25.0   plum|2026-11-20|5|6|20.0
--   Q4: apple|2026-11-01|10|9    apple|2026-11-10|12|15   apple|2026-11-25|15|6
--       kiwi|2026-12-01|3|0      pear|2026-11-01|20|14    pear|2026-11-15|18|16
--       plum|2026-11-01|5|19     plum|2026-11-20|6|11
--     (kiwi's only price starts after the reporting date: show 0, not a negative number.)

CREATE TABLE price_history (product TEXT, valid_from TEXT, price INTEGER,
                            PRIMARY KEY (product, valid_from));
INSERT INTO price_history VALUES
 ('apple', '2026-11-01', 10),
 ('apple', '2026-11-10', 12),
 ('apple', '2026-11-25', 15),
 ('pear',  '2026-11-01', 20),
 ('pear',  '2026-11-15', 18),
 ('plum',  '2026-11-01',  5),
 ('plum',  '2026-11-20',  6),
 ('kiwi',  '2026-12-01',  3);

CREATE TABLE orders (id INTEGER PRIMARY KEY, product TEXT, order_date TEXT, qty INTEGER);
INSERT INTO orders VALUES
 (1, 'apple', '2026-10-30', 4),
 (2, 'apple', '2026-11-01', 3),
 (3, 'apple', '2026-11-09', 2),
 (4, 'apple', '2026-11-10', 1),
 (5, 'apple', '2026-11-28', 4),
 (6, 'pear',  '2026-11-05', 5),
 (7, 'pear',  '2026-11-20', 2),
 (8, 'plum',  '2026-11-15', 1),
 (9, 'apple', '2026-11-24', 2);

-- Q1: turn the history into [valid_from, valid_to) ranges, then LEFT JOIN each order
--     to the range that contains its date (no match -> NULL price and total).
WITH ranges AS (
  SELECT product, valid_from, price,
         LEAD(valid_from) OVER (PARTITION BY product ORDER BY valid_from) AS valid_to
  FROM price_history
)
SELECT o.id, o.product, o.order_date,
       r.price         AS unit_price,
       r.price * o.qty AS line_total
FROM orders o
LEFT JOIN ranges r
  ON  r.product = o.product
  AND o.order_date >= r.valid_from
  AND (r.valid_to IS NULL OR o.order_date < r.valid_to)
ORDER BY o.id;

-- Q2: same as-of join, summed per product; every product from either table appears.
WITH ranges AS (
  SELECT product, valid_from, price,
         LEAD(valid_from) OVER (PARTITION BY product ORDER BY valid_from) AS valid_to
  FROM price_history
),
priced AS (
  SELECT o.product, r.price * o.qty AS line_total
  FROM orders o
  JOIN ranges r
    ON  r.product = o.product
    AND o.order_date >= r.valid_from
    AND (r.valid_to IS NULL OR o.order_date < r.valid_to)
),
products AS (
  SELECT product FROM price_history
  UNION
  SELECT product FROM orders
)
SELECT p.product, COALESCE(SUM(pr.line_total), 0) AS revenue
FROM products p
LEFT JOIN priced pr ON pr.product = p.product
GROUP BY p.product
ORDER BY revenue DESC, p.product;

-- Q3: compare each price with the previous one for the same product.
WITH changes AS (
  SELECT product, valid_from, price AS new_price,
         LAG(price) OVER (PARTITION BY product ORDER BY valid_from) AS old_price
  FROM price_history
)
SELECT product, valid_from, old_price, new_price,
       ROUND(100.0 * (new_price - old_price) / old_price, 1) AS pct_increase
FROM changes
WHERE old_price IS NOT NULL
  AND 10 * new_price > 11 * old_price          -- "more than 10%", in integer arithmetic
ORDER BY product, valid_from;

-- Q4: days each price was in effect; the open-ended price runs through 2026-11-30
--     (so it ends at 2026-12-01 exclusive). A price starting after that date gets 0.
WITH ranges AS (
  SELECT product, valid_from, price,
         COALESCE(LEAD(valid_from) OVER (PARTITION BY product ORDER BY valid_from),
                  DATE('2026-11-30', '+1 day')) AS valid_to
  FROM price_history
)
SELECT product, valid_from, price,
       MAX(0, CAST(JULIANDAY(valid_to) - JULIANDAY(valid_from) AS INTEGER)) AS days_in_effect
FROM ranges
ORDER BY product, valid_from;
