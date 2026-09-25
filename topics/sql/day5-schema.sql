-- Day 5 -- SQL: library loans (for CTE practice).
--
-- Load it with: sqlite3 practice_day5.db < day5-schema.sql

DROP TABLE IF EXISTS loans_sql;
DROP TABLE IF EXISTS books_sql;
DROP TABLE IF EXISTS authors_sql;

CREATE TABLE authors_sql (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE books_sql (
    id        INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    author_id INTEGER REFERENCES authors_sql(id)
);

CREATE TABLE loans_sql (
    id         INTEGER PRIMARY KEY,
    book_id    INTEGER REFERENCES books_sql(id),
    borrower   TEXT NOT NULL,
    loan_date  TEXT NOT NULL
);

INSERT INTO authors_sql (id, name) VALUES
    (1, 'Ursula Ilg'),
    (2, 'Marcus Chen'),
    (3, 'Priya Nair');

INSERT INTO books_sql (id, title, author_id) VALUES
    (1, 'The Glass Archive',      1),
    (2, 'Salt and Static',        1),
    (3, 'Nine Circuits',          2),
    (4, 'A Quiet Algorithm',      2),
    (5, 'Riverbed',               3);
-- note: Riverbed (id 5) has never been loaned -- deliberate, so
-- "average loan count across all books" has a zero in it.

INSERT INTO loans_sql (id, book_id, borrower, loan_date) VALUES
    (1, 1, 'Sam',   '2026-02-01'),
    (2, 1, 'Alex',  '2026-02-10'),
    (3, 1, 'Jordan','2026-02-20'),
    (4, 2, 'Sam',   '2026-02-05'),
    (5, 3, 'Alex',  '2026-02-08'),
    (6, 3, 'Dana',  '2026-02-15'),
    (7, 3, 'Priya', '2026-02-22'),
    (8, 4, 'Sam',   '2026-02-11');
-- note: Nine Circuits (id 3) has 3 loans, the most of any book, and
-- Ursula Ilg (author 1) has two books with loans (3 total) while
-- Marcus Chen (author 2) has two books with loans (4 total) -- useful
-- for the "combined loan count per author" query.
