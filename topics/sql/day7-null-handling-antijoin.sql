-- Day 7, Task 2 -- SQL: NULL handling (COALESCE, NULLIF) and anti-joins.
--
-- Self-contained: schema + data + queries all in this one file.
-- Load it with: sqlite3 practice_day7b.db < day7-null-handling-antijoin.sql
--
-- Nothing below is pre-solved. Write each query yourself.

DROP TABLE IF EXISTS purchases_sql;
DROP TABLE IF EXISTS shoppers_sql;

CREATE TABLE shoppers_sql (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE purchases_sql (
    id            INTEGER PRIMARY KEY,
    shopper_id    INTEGER NOT NULL REFERENCES shoppers_sql(id),
    amount        REAL NOT NULL,
    discount_pct  REAL   -- -1 is a legacy placeholder meaning "unknown", not a real 1% discount
);

INSERT INTO shoppers_sql (id, name, phone) VALUES
    (1, 'Amara', '555-0101'),
    (2, 'Ben',   NULL),
    (3, 'Chen',  '555-0103'),
    (4, 'Dana',  NULL),
    (5, 'Eli',   '555-0105');

INSERT INTO purchases_sql (id, shopper_id, amount, discount_pct) VALUES
    (1, 1, 50.0,  10),
    (2, 1, 30.0,  -1),
    (3, 2, 20.0,  0),
    (4, 3, 100.0, 15),
    (5, 3, 40.0,  -1);
-- note: shoppers 4 (Dana) and 5 (Eli) have NO rows in purchases_sql at
-- all -- that's deliberate, for Q1's anti-join. The -1 discount_pct
-- rows are deliberate too -- that's a legacy "we don't actually know"
-- placeholder some earlier import used instead of a real NULL.

-- Q1: List every shopper who has NEVER made a purchase (an
-- "anti-join" -- rows on the left with no match on the right). Use a
-- LEFT JOIN plus a WHERE clause checking for the absence of a match,
-- not a subquery.
SELECT s.id, s.name
FROM shoppers_sql s
LEFT JOIN purchases_sql p ON p.shopper_id = s.id
WHERE p.id IS NULL;


-- Q2: For EVERY shopper (including ones with zero purchases), show
-- their name, their phone with COALESCE(...) substituting 'N/A' for a
-- NULL phone, and their total spend with COALESCE(...) substituting 0
-- for a shopper with no purchases (a plain SUM() over a LEFT JOIN
-- would give NULL for those shoppers instead of 0).
SELECT
    s.name,
    COALESCE(s.phone, 'N/A') AS phone,
    COALESCE(SUM(p.amount), 0) AS total_spend
FROM shoppers_sql s
LEFT JOIN purchases_sql p ON p.shopper_id = s.id
GROUP BY s.id, s.name, s.phone;


-- Q3: For each shopper who has at least one purchase, show their name
-- and their AVERAGE discount_pct -- but treat any -1 placeholder as
-- unknown (i.e. NULLIF(discount_pct, -1) first, THEN average), so
-- those legacy rows are EXCLUDED from the average entirely instead of
-- dragging it down toward -1. (AVG() already ignores NULLs on its
-- own -- NULLIF is what turns the -1 placeholder into a real NULL in
-- the first place.)
SELECT
    s.name,
    AVG(NULLIF(p.discount_pct, -1)) AS avg_discount_pct
FROM shoppers_sql s
JOIN purchases_sql p ON p.shopper_id = s.id
GROUP BY s.id, s.name;
