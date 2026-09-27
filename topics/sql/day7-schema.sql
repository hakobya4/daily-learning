-- Day 7 -- SQL: daily temperature readings (for window-frame practice).
--
-- Load it with: sqlite3 practice_day7.db < day7-schema.sql

DROP TABLE IF EXISTS daily_readings_sql;

CREATE TABLE daily_readings_sql (
    id           INTEGER PRIMARY KEY,
    city         TEXT NOT NULL,
    reading_date TEXT NOT NULL,   -- 'YYYY-MM-DD'
    temp_c       REAL NOT NULL
);

INSERT INTO daily_readings_sql (id, city, reading_date, temp_c) VALUES
    (1,  'Ottawa',  '2026-05-01', 14),
    (2,  'Ottawa',  '2026-05-02', 16),
    (3,  'Ottawa',  '2026-05-03', 12),
    (4,  'Ottawa',  '2026-05-04', 18),
    (5,  'Ottawa',  '2026-05-05', 20),
    (6,  'Ottawa',  '2026-05-06', 15),
    (7,  'Halifax', '2026-05-01', 10),
    (8,  'Halifax', '2026-05-02', 9),
    (9,  'Halifax', '2026-05-03', 13),
    (10, 'Halifax', '2026-05-04', 11),
    (11, 'Halifax', '2026-05-05', 14),
    (12, 'Halifax', '2026-05-06', 12);
-- note: each city has exactly 6 rows across 6 consecutive dates -- that
-- regularity is what makes a "3-day moving average" easy to check by
-- hand (there's no gap in the dates to worry about).
