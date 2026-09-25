-- Day 5, Task 2 -- SQL: set operations (UNION, INTERSECT, EXCEPT).
--
-- Self-contained: schema + data + queries all in this one file
-- (like Day 4 Task 2, there's no separate schema file for this one).
-- Load it with: sqlite3 practice_day5b.db < day5-set-operations.sql
--
-- Nothing below is pre-solved. Write each query yourself.

DROP TABLE IF EXISTS python_devs_sql;
DROP TABLE IF EXISTS js_devs_sql;

CREATE TABLE python_devs_sql (
    name              TEXT NOT NULL,
    years_experience  INTEGER NOT NULL
);

CREATE TABLE js_devs_sql (
    name              TEXT NOT NULL,
    years_experience  INTEGER NOT NULL
);

INSERT INTO python_devs_sql (name, years_experience) VALUES
    ('Amir', 5),
    ('Beth', 2),
    ('Carlos', 7),
    ('Dana', 3);

INSERT INTO js_devs_sql (name, years_experience) VALUES
    ('Beth', 2),
    ('Carlos', 7),
    ('Eve', 1),
    ('Farid', 4);
-- note: Beth and Carlos know BOTH languages (they appear in both
-- tables, with the same years_experience in each) -- that's what
-- makes INTERSECT/EXCEPT interesting here.

-- Q1: List every name that appears in EITHER table (knows Python OR
-- JavaScript), with no duplicates. Use UNION (not UNION ALL -- add a
-- one-line comment explaining why UNION ALL would give a wrong answer
-- for THIS question specifically).
-- TODO: write this query.


-- Q2: List every name that appears in BOTH tables (knows both
-- languages). Use INTERSECT.
-- TODO: write this query.


-- Q3: List every Python developer who does NOT also appear in the JS
-- developers table (Python-only devs). Use EXCEPT.
-- TODO: write this query.


-- Q4: Using UNION ALL (deliberately, this time) plus GROUP BY and
-- SUM(), compute each name's TOTAL years of experience added across
-- both tables -- someone who appears in both tables should have their
-- two years_experience values summed, not just one of them shown.
-- TODO: write this query.
