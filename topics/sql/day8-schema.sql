-- Day 8 -- SQL: delivery records (for date/time + string-aggregation practice).
--
-- Load it with: sqlite3 practice_day8.db < day8-schema.sql

DROP TABLE IF EXISTS deliveries_sql;

CREATE TABLE deliveries_sql (
    id           INTEGER PRIMARY KEY,
    driver       TEXT NOT NULL,
    region       TEXT NOT NULL,
    delivered_at TEXT NOT NULL   -- 'YYYY-MM-DD'
);

INSERT INTO deliveries_sql (id, driver, region, delivered_at) VALUES
    (1, 'Amara', 'North', '2026-06-01'),
    (2, 'Ben',   'North', '2026-06-03'),
    (3, 'Chen',  'South', '2026-06-02'),
    (4, 'Dana',  'South', '2026-06-10'),
    (5, 'Eli',   'North', '2026-06-12'),
    (6, 'Farah', 'South', '2026-05-28'),
    (7, 'Gus',   'North', '2026-06-15'),
    (8, 'Hana',  'South', '2026-06-14');
-- note: one delivery (Farah, id 6) is in May, everything else is in
-- June -- that split is what makes the month-grouping query in Q2
-- checkable by hand. The dates cluster around 2026-06-15 deliberately,
-- for Q3's "within the last 7 days of a reference date" window.
