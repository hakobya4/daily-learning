-- Day 5, Task 1 -- SQL: Common Table Expressions (CTEs).
-- Schema: day5-schema.sql (authors_sql, books_sql, loans_sql)
--
-- Nothing below is pre-solved. Write each query yourself.

-- Q1: Using a CTE that computes the number of loans per book, list
-- every book's title alongside its loan count, but only for books
-- loaned MORE THAN the average loan count across ALL books (books
-- with zero loans still count toward that average). Compute the
-- average from the same CTE, not a separate query.
-- TODO: write this query (WITH loan_counts AS (...) SELECT ...).


-- Q2: Using a CTE plus ROW_NUMBER(), find each author's single
-- MOST-LOANED book (author name, book title, loan count). An author
-- with no loaned books at all can be omitted from the result.
-- TODO: write this query.


-- Q3: Using a CTE, list every author who has written MORE THAN ONE
-- book AND whose books' loans, summed together, total more than 3.
-- TODO: write this query.
