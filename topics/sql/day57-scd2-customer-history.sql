-- Day 57, Task 3 -- SQL: build a Type-2 slowly changing dimension and join facts "as of".
--
-- Self-contained. Load with: sqlite3 practice_day57.db < day57-scd2-customer-history.sql
-- (needs window functions: SQLite >= 3.25, or any PostgreSQL / MySQL 8).
--
-- THE PROBLEM
-- customer_changes(change_id, customer_id, changed_on, city, tier) is a raw change feed:
-- every row is the customer's FULL state (city + tier) starting on changed_on. It is
-- noisy:
--   * some rows repeat the previous state exactly (no-op re-sends) -- they must NOT
--     start a new version;
--   * several rows can share the same (customer_id, changed_on) -- only the one with
--     the HIGHEST change_id counts for that day (earlier ones that day are discarded
--     BEFORE the no-op check).
-- orders(order_id, customer_id, ordered_on, amount) are facts that must be attributed
-- to the customer's state ON THE ORDER DATE.
-- Write 4 queries below the data. No procedural code, no recursive CTEs needed.
-- Nothing pre-solved.
--
-- Q1: The SCD2 dimension: customer_id, version_no (1, 2, 3... per customer, no gaps),
--     city, tier, valid_from, valid_to (EXCLUSIVE end = next version's valid_from,
--     NULL for the current version), is_current (1/0). Order by customer_id, version_no.
--     Hint: ROW_NUMBER() per (customer, day) to keep the last change of a day, then
--     LAG(city)/LAG(tier) to drop no-ops, then ROW_NUMBER() + LEAD(changed_on).
-- Q2: Point-in-time attribution: order_id, customer_id, city, tier as of ordered_on
--     (valid_from <= ordered_on < valid_to, open-ended if valid_to IS NULL). Orders
--     placed BEFORE the customer's first version get city = tier = 'unknown'.
--     Every order appears. Order by order_id.
-- Q3: Revenue per tier two ways: tier, revenue_at_order_time (tier from Q2),
--     revenue_by_current_tier (tier of the customer's CURRENT version). Include every
--     tier that appears anywhere in customer_changes plus 'unknown'; show 0, not NULL.
--     Order by tier.
-- Q4: Customers who MOVED (city changed between consecutive versions of Q1) at least
--     twice: customer_id, city_changes. Tier-only versions don't count as moves.
--     Order by customer_id.
--
-- Expected results for the data below:
--   Q1: 10|1|Yerevan|basic|2026-01-01|2026-05-15|0
--       10|2|Yerevan|gold|2026-05-15|2026-08-01|0
--       10|3|Toronto|gold|2026-08-01||1
--       20|1|Gyumri|basic|2026-02-10|2026-04-01|0
--       20|2|Toronto|basic|2026-04-01|2026-06-01|0
--       20|3|Gyumri|silver|2026-06-01||1
--       30|1|Montreal|basic|2026-07-01||1
--   Q2: 1001|10|Yerevan|basic   1002|10|Yerevan|gold    1003|10|Toronto|gold
--       1004|20|unknown|unknown 1005|20|Toronto|basic   1006|20|Toronto|basic
--       1007|20|Gyumri|silver   1008|30|Montreal|basic
--   Q3: basic|310|70   gold|550|650   silver|120|300   unknown|40|0
--   Q4: 20|2

CREATE TABLE customer_changes (change_id INTEGER PRIMARY KEY, customer_id INTEGER,
                               changed_on TEXT, city TEXT, tier TEXT);
INSERT INTO customer_changes VALUES
 (1,  10, '2026-01-01', 'Yerevan',  'basic'),
 (2,  10, '2026-03-01', 'Yerevan',  'basic'),
 (3,  10, '2026-05-15', 'Yerevan',  'gold'),
 (4,  10, '2026-08-01', 'Toronto',  'gold'),
 (5,  20, '2026-02-10', 'Gyumri',   'basic'),
 (6,  20, '2026-04-01', 'Toronto',  'basic'),
 (7,  20, '2026-06-01', 'Gyumri',   'basic'),
 (8,  20, '2026-06-01', 'Gyumri',   'silver'),
 (9,  30, '2026-07-01', 'Montreal', 'basic'),
 (10, 30, '2026-09-01', 'Montreal', 'basic');

CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER,
                     ordered_on TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1001, 10, '2026-02-01', 100),
 (1002, 10, '2026-05-15', 250),
 (1003, 10, '2026-09-30', 300),
 (1004, 20, '2026-01-31',  40),
 (1005, 20, '2026-04-01',  80),
 (1006, 20, '2026-05-31',  60),
 (1007, 20, '2026-06-02', 120),
 (1008, 30, '2026-10-01',  70);

-- Q1
WITH last_of_day AS (
  SELECT customer_id, changed_on, city, tier,
         ROW_NUMBER() OVER (PARTITION BY customer_id, changed_on
                            ORDER BY change_id DESC) AS rn
  FROM customer_changes
),
daily AS (
  SELECT customer_id, changed_on, city, tier,
         LAG(city) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_city,
         LAG(tier) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_tier
  FROM last_of_day
  WHERE rn = 1
),
changes AS (
  SELECT customer_id, changed_on, city, tier
  FROM daily
  WHERE prev_city IS NULL OR city <> prev_city OR tier <> prev_tier
),
scd AS (
  SELECT customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY changed_on) AS version_no,
         city, tier,
         changed_on AS valid_from,
         LEAD(changed_on) OVER (PARTITION BY customer_id ORDER BY changed_on) AS valid_to
  FROM changes
)
SELECT customer_id, version_no, city, tier, valid_from, valid_to,
       CASE WHEN valid_to IS NULL THEN 1 ELSE 0 END AS is_current
FROM scd
ORDER BY customer_id, version_no;

-- Q2
WITH last_of_day AS (
  SELECT customer_id, changed_on, city, tier,
         ROW_NUMBER() OVER (PARTITION BY customer_id, changed_on
                            ORDER BY change_id DESC) AS rn
  FROM customer_changes
),
daily AS (
  SELECT customer_id, changed_on, city, tier,
         LAG(city) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_city,
         LAG(tier) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_tier
  FROM last_of_day
  WHERE rn = 1
),
changes AS (
  SELECT customer_id, changed_on, city, tier
  FROM daily
  WHERE prev_city IS NULL OR city <> prev_city OR tier <> prev_tier
),
scd AS (
  SELECT customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY changed_on) AS version_no,
         city, tier,
         changed_on AS valid_from,
         LEAD(changed_on) OVER (PARTITION BY customer_id ORDER BY changed_on) AS valid_to
  FROM changes
),
attributed AS (
  SELECT o.order_id, o.customer_id, o.amount,
         COALESCE(s.city, 'unknown') AS city,
         COALESCE(s.tier, 'unknown') AS tier
  FROM orders o
  LEFT JOIN scd s
    ON s.customer_id = o.customer_id
   AND s.valid_from <= o.ordered_on
   AND (s.valid_to IS NULL OR o.ordered_on < s.valid_to)
)
SELECT order_id, customer_id, city, tier
FROM attributed
ORDER BY order_id;

-- Q3
WITH last_of_day AS (
  SELECT customer_id, changed_on, city, tier,
         ROW_NUMBER() OVER (PARTITION BY customer_id, changed_on
                            ORDER BY change_id DESC) AS rn
  FROM customer_changes
),
daily AS (
  SELECT customer_id, changed_on, city, tier,
         LAG(city) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_city,
         LAG(tier) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_tier
  FROM last_of_day
  WHERE rn = 1
),
changes AS (
  SELECT customer_id, changed_on, city, tier
  FROM daily
  WHERE prev_city IS NULL OR city <> prev_city OR tier <> prev_tier
),
scd AS (
  SELECT customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY changed_on) AS version_no,
         city, tier,
         changed_on AS valid_from,
         LEAD(changed_on) OVER (PARTITION BY customer_id ORDER BY changed_on) AS valid_to
  FROM changes
),
attributed AS (
  SELECT o.order_id, o.customer_id, o.amount,
         COALESCE(s.city, 'unknown') AS city,
         COALESCE(s.tier, 'unknown') AS tier
  FROM orders o
  LEFT JOIN scd s
    ON s.customer_id = o.customer_id
   AND s.valid_from <= o.ordered_on
   AND (s.valid_to IS NULL OR o.ordered_on < s.valid_to)
),
tiers AS (
  SELECT DISTINCT tier FROM customer_changes
  UNION
  SELECT 'unknown'
),
current_tier AS (
  SELECT customer_id, tier FROM scd WHERE valid_to IS NULL
)
SELECT t.tier,
       COALESCE((SELECT SUM(a.amount) FROM attributed a WHERE a.tier = t.tier), 0)
         AS revenue_at_order_time,
       COALESCE((SELECT SUM(o.amount)
                 FROM orders o JOIN current_tier c ON c.customer_id = o.customer_id
                 WHERE c.tier = t.tier), 0)
         AS revenue_by_current_tier
FROM tiers t
ORDER BY t.tier;

-- Q4
WITH last_of_day AS (
  SELECT customer_id, changed_on, city, tier,
         ROW_NUMBER() OVER (PARTITION BY customer_id, changed_on
                            ORDER BY change_id DESC) AS rn
  FROM customer_changes
),
daily AS (
  SELECT customer_id, changed_on, city, tier,
         LAG(city) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_city,
         LAG(tier) OVER (PARTITION BY customer_id ORDER BY changed_on) AS prev_tier
  FROM last_of_day
  WHERE rn = 1
),
changes AS (
  SELECT customer_id, changed_on, city, tier
  FROM daily
  WHERE prev_city IS NULL OR city <> prev_city OR tier <> prev_tier
),
scd AS (
  SELECT customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY changed_on) AS version_no,
         city, tier,
         changed_on AS valid_from,
         LEAD(changed_on) OVER (PARTITION BY customer_id ORDER BY changed_on) AS valid_to
  FROM changes
),
moves AS (
  SELECT customer_id, city,
         LAG(city) OVER (PARTITION BY customer_id ORDER BY version_no) AS prev_city
  FROM scd
)
SELECT customer_id, COUNT(*) AS city_changes
FROM moves
WHERE prev_city IS NOT NULL AND city <> prev_city
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY customer_id;
