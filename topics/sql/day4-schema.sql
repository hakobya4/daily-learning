-- Day 4 -- SQL: window functions (products & sales).
--
-- Load it with: sqlite3 practice_day4.db < day4-schema.sql
USE db_narekhak;
DROP TABLE IF EXISTS sales_sql;
DROP TABLE IF EXISTS products_sql;

CREATE TABLE products_sql (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    category TEXT NOT NULL,
    price    REAL NOT NULL
);

CREATE TABLE sales_sql (
    id          INTEGER PRIMARY KEY,
    product_id  INTEGER REFERENCES products_sql(id),
    quantity    INTEGER NOT NULL,
    sale_date   TEXT NOT NULL
);

INSERT INTO products_sql (id, name, category, price) VALUES
    (1, 'Widget',       'Hardware', 9.99),
    (2, 'Gadget',       'Hardware', 19.99),
    (3, 'Notebook',     'Office',   4.50),
    (4, 'Pen Pack',     'Office',   2.25),
    (5, 'Desk Lamp',    'Hardware', 24.99),
    (6, 'Sticky Notes', 'Office',   3.00);

INSERT INTO sales_sql (id, product_id, quantity, sale_date) VALUES
    (1,  1, 10, '2026-01-05'),
    (2,  1, 15, '2026-01-12'),
    (3,  2, 5,  '2026-01-06'),
    (4,  2, 8,  '2026-01-20'),
    (5,  3, 20, '2026-01-03'),
    (6,  3, 12, '2026-01-15'),
    (7,  4, 30, '2026-01-04'),
    (8,  5, 3,  '2026-01-10'),
    (9,  6, 25, '2026-01-08'),
    (10, 6, 18, '2026-01-22');
-- note: two products per category get more than one sale
-- (Widget/Gadget and Notebook/Sticky Notes), which is what makes the
-- PARTITION BY category window queries below interesting.
