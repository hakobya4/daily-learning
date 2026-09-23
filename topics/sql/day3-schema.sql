-- Day 3 -- SQL / CS fundamentals: employees & departments (self-joins,
-- aggregation with HAVING, and NULL-safe filtering).
--
-- Load it with: sqlite3 practice_day3.db < day3-schema.sql

DROP TABLE IF EXISTS employees_sql;
DROP TABLE IF EXISTS departments_sql;

CREATE TABLE departments_sql (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL
);

CREATE TABLE employees_sql (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    department_id INTEGER REFERENCES departments_sql(id),
    manager_id    INTEGER REFERENCES employees_sql(id),
    salary        REAL NOT NULL
);

INSERT INTO departments_sql (id, name) VALUES
    (1, 'Engineering'),
    (2, 'Sales'),
    (3, 'Support');

INSERT INTO employees_sql (id, name, department_id, manager_id, salary) VALUES
    (1, 'Priya',  1, NULL, 120000),
    (2, 'Sam',    1, 1,    95000),
    (3, 'Jordan', 1, 1,    88000),
    (4, 'Alex',   2, NULL, 90000),
    (5, 'Dana',   2, 4,    60000),
    (6, 'Chris',  3, NULL, 55000);
-- note: Chris has no manager and no direct reports; Engineering has
-- one manager (Priya) with two reports.
