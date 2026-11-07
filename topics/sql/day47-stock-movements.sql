-- Day 47, Task 6 -- SQL: running balance, latest row per group, first-event-or-NULL.
--
-- Self-contained. Load with: sqlite3 practice_day47.db < day47-stock-movements.sql
--
-- THE PROBLEM
-- items(id, name), movements(item_id, day, delta). delta > 0 is stock in, < 0 stock out.
-- Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Running balance per item ordered by day. Output: name, day, balance.
--     Order by name, day.   Hint: SUM(delta) OVER (PARTITION BY item_id ORDER BY day).
-- Q2: The most recent movement per item. Output: name, day, delta. Order by name.
--     Hint: ROW_NUMBER() OVER (PARTITION BY item_id ORDER BY day DESC) = 1.
-- Q3: Names of items whose balance was EVER negative. Order by name.
-- Q4: For EVERY item (even ones that never went negative) the first day its balance
--     went negative, or NULL. Output: name, first_negative_day. Order by name.
--     Hint: reuse the Q1 logic in a CTE, then LEFT JOIN / MIN(CASE WHEN balance < 0 ...).
--
-- Expected results for the data below:
--   Q1: bolt|2026-01-01|10  bolt|2026-01-03|6  bolt|2026-01-05|-2  bolt|2026-01-06|3
--       nut|2026-01-02|20  nut|2026-01-04|15
--       washer|2026-01-03|-1  washer|2026-01-04|6
--   Q2: bolt|2026-01-06|5  nut|2026-01-04|-5  washer|2026-01-04|7
--   Q3: bolt  washer
--   Q4: bolt|2026-01-05  nut|(NULL)  washer|2026-01-03

CREATE TABLE items (id INTEGER, name TEXT);
INSERT INTO items VALUES (1,'bolt'),(2,'nut'),(3,'washer');
CREATE TABLE movements (item_id INTEGER, day TEXT, delta INTEGER);
INSERT INTO movements VALUES
 (1,'2026-01-01',10),(1,'2026-01-03',-4),(1,'2026-01-05',-8),(1,'2026-01-06',5),
 (2,'2026-01-02',20),(2,'2026-01-04',-5),
 (3,'2026-01-03',-1),(3,'2026-01-04',7);

-- Q1
SELECT i.name, m.day,
       SUM(m.delta) OVER (PARTITION BY m.item_id ORDER BY m.day) AS balance
FROM movements m JOIN items i ON i.id = m.item_id
ORDER BY i.name, m.day;

-- Q2
SELECT name, day, delta FROM (
  SELECT i.name, m.day, m.delta,
         ROW_NUMBER() OVER (PARTITION BY m.item_id ORDER BY m.day DESC) AS rn
  FROM movements m JOIN items i ON i.id = m.item_id
) WHERE rn = 1
ORDER BY name;

-- Q3
WITH run AS (
  SELECT item_id,
         SUM(delta) OVER (PARTITION BY item_id ORDER BY day) AS balance
  FROM movements
)
SELECT DISTINCT i.name
FROM run JOIN items i ON i.id = run.item_id
WHERE run.balance < 0
ORDER BY i.name;

-- Q4
WITH run AS (
  SELECT item_id, day,
         SUM(delta) OVER (PARTITION BY item_id ORDER BY day) AS balance
  FROM movements
)
SELECT i.name,
       (SELECT MIN(r.day) FROM run r WHERE r.item_id = i.id AND r.balance < 0) AS first_negative_day
FROM items i
ORDER BY i.name;
