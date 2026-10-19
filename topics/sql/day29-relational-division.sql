-- Day 29, Task 1 -- SQL: relational division ("bought EVERY product in a set").
--
-- Self-contained. Load with: sqlite3 practice_day29.db < day29-relational-division.sql
--
-- THE PROBLEM
-- purchases(customer, product) lists what each customer bought (may repeat).
-- required(product) is a set of products. Write 3 queries. Nothing pre-solved.
--
-- Q1: Customers who bought ALL products in required. Output: customer.
--     Order by customer.
-- Q2: Customers who bought ALL required products and NOTHING else.
--     Output: customer. Order by customer.
-- Q3: For every customer, how many required products they are MISSING.
--     Output: customer, missing (0 for complete customers). Include
--     customers who bought none of the required products. Order by
--     missing, customer.
--
-- HINT: Q1: GROUP BY customer HAVING COUNT(DISTINCT product) over only the
-- required rows = (SELECT COUNT(*) FROM required). Q2 additionally compares
-- against the customer's total distinct products. Q3: required count minus
-- the customer's matched count.
--
-- Expected results for the data below:
--   Q1: ana, cy
--   Q2: cy
--   Q3: ana 0 / cy 0 / ben 1 / dee 3 (ordered by missing, customer)

DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS required;
CREATE TABLE purchases (customer TEXT NOT NULL, product TEXT NOT NULL);
CREATE TABLE required  (product TEXT PRIMARY KEY);
INSERT INTO required (product) VALUES ('pen'), ('ink'), ('pad');
INSERT INTO purchases (customer, product) VALUES
    ('ana', 'pen'), ('ana', 'ink'), ('ana', 'pad'), ('ana', 'tape'),
    ('ben', 'pen'), ('ben', 'ink'), ('ben', 'ink'),
    ('cy',  'pad'), ('cy',  'pen'), ('cy',  'ink'), ('cy', 'pen'),
    ('dee', 'tape');

-- TODO Q1


-- TODO Q2


-- TODO Q3

