-- Day 2 -- SQL / CS fundamentals: joins, aggregation, and NULL handling.
--
-- A tiny bookstore schema: customers who may or may not have placed orders.
-- Load it with: sqlite3 practice.db < schema.sql
-- (sqlite3 ships with macOS by default, no install needed.)

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    city    TEXT NOT NULL
);

CREATE TABLE orders (
    id            INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(id),
    order_date    TEXT NOT NULL,   -- 'YYYY-MM-DD'
    amount        REAL NOT NULL
);

INSERT INTO customers (id, name, city) VALUES
    (1, 'Alice', 'Toronto'),
    (2, 'Bob',   'Toronto'),
    (3, 'Carol', 'Vancouver'),
    (4, 'Dave',  'Montreal'),
    (5, 'Erin',  'Toronto');   -- note: Erin has never ordered anything

INSERT INTO orders (id, customer_id, order_date, amount) VALUES
    (1, 1, '2026-01-05', 120.50),
    (2, 1, '2026-03-12', 45.00),
    (3, 2, '2026-02-20', 300.00),
    (4, 3, '2026-01-15', 75.25),
    (5, 4, '2026-04-01', 500.00),
    (6, 1, '2026-05-01', 60.00);
