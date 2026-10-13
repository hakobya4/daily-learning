-- Day 23, Task 1 -- SQL: overlapping bookings and max concurrency.
--
-- Self-contained. Load with: sqlite3 practice_day23.db < day23-bookings-overlap.sql
--
-- THE PROBLEM
-- bookings_sql has one row per room booking: [start_ts, end_ts) in
-- 'YYYY-MM-DD HH:MM' text. Intervals are half-open: a booking that ends at
-- 10:00 does NOT overlap one that starts at 10:00. Write 3 queries.
-- Nothing pre-solved.
--
-- Q1: All overlapping pairs in the same room: room, id_a, id_b with
--     id_a < id_b. Order by room, id_a, id_b.
-- Q2: For each room, the maximum number of bookings active at the same
--     moment: room, max_concurrent. Order by room.
-- Q3: Rooms that have NO overlap at all between their bookings:
--     room. Order by room.
--
-- HINT: two intervals overlap iff a.start < b.end AND b.start < a.end.
-- For Q2, the max concurrency is always reached at some booking's start:
-- for each booking, count bookings in the room with start <= its start
-- AND end > its start, then take MAX per room.

DROP TABLE IF EXISTS bookings_sql;
CREATE TABLE bookings_sql (
    id       INTEGER PRIMARY KEY,
    room     TEXT NOT NULL,
    start_ts TEXT NOT NULL,
    end_ts   TEXT NOT NULL
);
INSERT INTO bookings_sql (id, room, start_ts, end_ts) VALUES
    (1, 'A', '2026-10-01 09:00', '2026-10-01 10:00'),
    (2, 'A', '2026-10-01 09:30', '2026-10-01 11:00'),
    (3, 'A', '2026-10-01 10:30', '2026-10-01 12:00'),
    (4, 'A', '2026-10-01 12:00', '2026-10-01 13:00'),
    (5, 'B', '2026-10-01 09:00', '2026-10-01 10:00'),
    (6, 'B', '2026-10-01 10:00', '2026-10-01 11:00'),
    (7, 'B', '2026-10-01 11:00', '2026-10-01 12:00'),
    (8, 'C', '2026-10-01 14:00', '2026-10-01 18:00'),
    (9, 'C', '2026-10-01 15:00', '2026-10-01 16:00'),
    (10,'C', '2026-10-01 15:30', '2026-10-01 17:00'),
    (11,'D', '2026-10-02 08:00', '2026-10-02 09:00');

-- Q1:

-- Q2:

-- Q3:
