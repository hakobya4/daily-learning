-- Day 6 -- SQL: employee org chart (for recursive CTE practice).
--
-- Load it with: sqlite3 practice_day6.db < day6-schema.sql

DROP TABLE IF EXISTS employees_org_sql;

CREATE TABLE employees_org_sql (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER REFERENCES employees_org_sql(id)
);

INSERT INTO employees_org_sql (id, name, manager_id) VALUES
    (1, 'Rosa',  NULL),  -- CEO, no manager
    (2, 'Malik', 1),     -- VP of Engineering, reports to Rosa
    (3, 'Tara',  1),     -- VP of Sales, reports to Rosa
    (4, 'Owen',  2),     -- Manager, reports to Malik
    (5, 'Nina',  2),     -- Manager, reports to Malik
    (6, 'Kai',   4),     -- IC, reports to Owen
    (7, 'Leo',   4),     -- IC, reports to Owen
    (8, 'Sara',  3);     -- IC, reports directly to Tara
-- note: Malik's org (Owen, Nina, Kai, Leo) is 4 people deep across two
-- levels -- that's what makes the "all reports under a manager" query
-- interesting, since Kai and Leo only show up via Owen, not directly
-- under Malik.
