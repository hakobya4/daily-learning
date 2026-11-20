-- Day 60, Task 3 -- SQL: hotel occupancy -- expanding stays into nights, overlaps, ADR.
--
-- Self-contained. Load with: sqlite3 practice_day60.db < day60-hotel-occupancy-nights.sql
-- (SQLite >= 3.25 for window functions; recursive CTEs work in any modern SQLite).
-- No sqlite3 CLI? python3 -c "import sqlite3; ..." runs it just as well.
--
-- THE PROBLEM
-- rooms(room_id, room_type)  and
-- bookings(booking_id, room_id, guest, check_in, check_out, nightly_rate, status)
-- check_in / check_out are 'YYYY-MM-DD'. A stay occupies the NIGHTS check_in,
-- check_in + 1, ..., check_out - 1 (the check-out date itself is NOT a night).
-- Only status = 'confirmed' counts anywhere below; 'cancelled' rows are ignored.
-- The reporting window is the 7 nights 2026-12-01 .. 2026-12-07 (inclusive).
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Nightly occupancy for every night of the window -- including nights with nobody:
--     night, rooms_occupied (DISTINCT rooms with a confirmed stay that night),
--     occupancy_pct = ROUND(100.0 * rooms_occupied / (SELECT COUNT(*) FROM rooms), 1),
--     ordered by night.
--     Hint: WITH RECURSIVE nights(night) AS (SELECT '2026-12-01' UNION ALL
--     SELECT date(night, '+1 day') FROM nights WHERE night < '2026-12-07'), then LEFT JOIN
--     bookings ON night >= check_in AND night < check_out.
-- Q2: Double bookings: pairs of confirmed bookings for the SAME room whose stays share at
--     least one night (a.check_in < b.check_out AND b.check_in < a.check_out), each pair
--     once with a.booking_id < b.booking_id. Output room_id, booking_a, booking_b,
--     overlap_nights (number of shared nights; julianday() differences, cast to INTEGER),
--     ordered by room_id, booking_a, booking_b. (Not restricted to the window.)
-- Q3: Per room_type, inside the window only (clip every stay to 2026-12-01 .. 2026-12-08
--     check-out): nights_sold, revenue = SUM(clipped nights * nightly_rate),
--     adr = ROUND(revenue * 1.0 / nights_sold, 2) (average daily rate), and
--     rank_by_revenue (RANK() over revenue DESC). Include only room types that sold at
--     least one night in the window. Order by rank_by_revenue, then room_type.
--     Hint: clipped nights = julianday(MIN(check_out, '2026-12-08'))
--                          - julianday(MAX(check_in, '2026-12-01')), keep it only if > 0
--     (scalar MIN/MAX with two arguments work on these ISO date strings).
--
-- Expected results for the data below:
--   Q1: 2026-12-01|2|33.3
--       2026-12-02|2|33.3
--       2026-12-03|4|66.7
--       2026-12-04|4|66.7
--       2026-12-05|2|33.3
--       2026-12-06|2|33.3
--       2026-12-07|1|16.7
--   Q2: 102|5|6|2
--       104|9|11|1
--   Q3: double|12|2095|174.58|1
--       suite|5|2000|400.0|2
--       single|3|270|90.0|3

CREATE TABLE rooms (room_id INTEGER PRIMARY KEY, room_type TEXT);
INSERT INTO rooms VALUES
 (101, 'single'), (102, 'double'), (103, 'double'),
 (104, 'suite'),  (105, 'single'), (106, 'double');

CREATE TABLE bookings (
  booking_id   INTEGER PRIMARY KEY,
  room_id      INTEGER REFERENCES rooms(room_id),
  guest        TEXT,
  check_in     TEXT,
  check_out    TEXT,
  nightly_rate INTEGER,
  status       TEXT
);
INSERT INTO bookings VALUES
 (1,  101, 'Ana',   '2026-11-28', '2026-12-02', 90,  'confirmed'),  -- starts before the window
 (2,  102, 'Ben',   '2026-12-01', '2026-12-03', 180, 'confirmed'),
 (3,  103, 'Cleo',  '2026-12-02', '2026-12-05', 170, 'confirmed'),
 (4,  103, 'Dev',   '2026-12-05', '2026-12-06', 160, 'cancelled'),  -- cancelled: ignored
 (5,  102, 'Eli',   '2026-12-03', '2026-12-06', 175, 'confirmed'),
 (6,  102, 'Fay',   '2026-12-04', '2026-12-08', 175, 'confirmed'),  -- overlaps booking 5
 (7,  105, 'Gus',   '2026-12-03', '2026-12-05', 90,  'confirmed'),
 (8,  101, 'Hana',  '2026-12-02', '2026-12-02', 90,  'confirmed'),  -- zero nights
 (9,  104, 'Ivo',   '2026-12-03', '2026-12-06', 400, 'confirmed'),
 (10, 106, 'Jade',  '2026-12-09', '2026-12-12', 150, 'confirmed'),  -- after the window
 (11, 104, 'Kai',   '2026-12-05', '2026-12-07', 400, 'confirmed'),  -- overlaps booking 9
 (12, 105, 'Lea',   '2026-12-04', '2026-12-08', 95,  'cancelled'),  -- cancelled: ignored
 (13, 103, 'Mo',    '2026-11-20', '2026-11-25', 150, 'confirmed');  -- before the window

-- Q1: nightly occupancy
-- TODO: write your query here


-- Q2: double bookings
-- TODO: write your query here


-- Q3: room-type revenue and ADR inside the window
-- TODO: write your query here
