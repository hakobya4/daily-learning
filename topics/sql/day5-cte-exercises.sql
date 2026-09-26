-- Day 5, Task 1 -- SQL: Common Table Expressions (CTEs).
-- Schema: day5-schema.sql (authors_sql, books_sql, loans_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: Using a CTE that computes the number of loans per book, list
-- every book's title alongside its loan count, but only for books
-- loaned MORE THAN the average loan count across ALL books (books
-- with zero loans still count toward that average). Compute the
-- average from the same CTE, not a separate query.
WITH loan_counts AS (
    SELECT
        b.id AS book_id,
        b.title AS title,
        COUNT(l.id) AS loan_count
    FROM books_sql b
    LEFT JOIN loans_sql l ON l.book_id = b.id
    GROUP BY b.id, b.title
)
SELECT title, loan_count
FROM loan_counts
WHERE loan_count > (SELECT AVG(loan_count) FROM loan_counts)
ORDER BY loan_count DESC, title;


-- Q2: Using a CTE plus ROW_NUMBER(), find each author's single
-- MOST-LOANED book (author name, book title, loan count). An author
-- with no loaned books at all can be omitted from the result.
WITH book_loan_counts AS (
    SELECT
        b.id AS book_id,
        b.title AS title,
        b.author_id AS author_id,
        COUNT(l.id) AS loan_count
    FROM books_sql b
    LEFT JOIN loans_sql l ON l.book_id = b.id
    GROUP BY b.id, b.title, b.author_id
),
ranked AS (
    SELECT
        book_id, title, author_id, loan_count,
        ROW_NUMBER() OVER (
            PARTITION BY author_id
            ORDER BY loan_count DESC, title
        ) AS rn
    FROM book_loan_counts
    WHERE loan_count > 0
)
SELECT a.name AS author_name, r.title AS book_title, r.loan_count
FROM ranked r
JOIN authors_sql a ON a.id = r.author_id
WHERE r.rn = 1
ORDER BY a.name;


-- Q3: Using a CTE, list every author who has written MORE THAN ONE
-- book AND whose books' loans, summed together, total more than 3.
WITH author_loan_totals AS (
    SELECT
        a.id AS author_id,
        a.name AS author_name,
        COUNT(DISTINCT b.id) AS book_count,
        COUNT(l.id) AS total_loans
    FROM authors_sql a
    JOIN books_sql b ON b.author_id = a.id
    LEFT JOIN loans_sql l ON l.book_id = b.id
    GROUP BY a.id, a.name
)
SELECT author_name, book_count, total_loans
FROM author_loan_totals
WHERE book_count > 1 AND total_loans > 3
ORDER BY author_name;
