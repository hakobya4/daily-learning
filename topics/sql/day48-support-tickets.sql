-- Day 48, Task 6 -- SQL: LEFT JOIN with filter in ON, date arithmetic, top row per group, NOT EXISTS.
--
-- Self-contained. Load with: sqlite3 practice_day48.db < day48-support-tickets.sql
--
-- THE PROBLEM
-- agents(id, name), tickets(id, agent_id, opened, closed, priority). closed is NULL while
-- a ticket is still open. Dates are ISO text. Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Open-ticket count per agent, INCLUDING agents with zero. Output: name, open_tickets.
--     Order by name.   Hint: put "closed IS NULL" in the LEFT JOIN's ON clause, not WHERE.
-- Q2: Average days-to-close (closed tickets only) per agent, rounded to 2 decimals, agents
--     with no closed ticket omitted. Output: name, avg_days. Order by avg_days DESC.
--     Hint: julianday(closed) - julianday(opened).
-- Q3: Each agent's slowest closed ticket (ties: lowest ticket id). Output: name, id, days.
--     Order by name.   Hint: ROW_NUMBER() OVER (PARTITION BY agent ORDER BY days DESC, id).
-- Q4: Agents for whom EVERY high-priority ticket was closed within 2 days (a still-open
--     high ticket disqualifies; an agent with no high tickets qualifies). Output: name.
--     Order by name.   Hint: NOT EXISTS a "bad" high ticket.
--
-- Expected results for the data below:
--   Q1: li|0  maya|0  omar|2
--   Q2: omar|4.5  maya|3.33
--   Q3: maya|2|7  omar|6|8
--   Q4: li  maya

CREATE TABLE agents (id INTEGER, name TEXT);
INSERT INTO agents VALUES (1,'maya'),(2,'omar'),(3,'li');
CREATE TABLE tickets (id INTEGER, agent_id INTEGER, opened TEXT, closed TEXT, priority TEXT);
INSERT INTO tickets VALUES
 (1,1,'2026-02-01','2026-02-03','high'),
 (2,1,'2026-02-02','2026-02-09','low'),
 (3,1,'2026-02-10','2026-02-11','high'),
 (4,2,'2026-02-01','2026-02-02','low'),
 (5,2,'2026-02-03',NULL,'high'),
 (6,2,'2026-02-04','2026-02-12','high'),
 (7,2,'2026-02-05',NULL,'low');

-- Q1
SELECT a.name, COUNT(t.id) AS open_tickets
FROM agents a
LEFT JOIN tickets t ON t.agent_id = a.id AND t.closed IS NULL
GROUP BY a.id, a.name
ORDER BY a.name;

-- Q2
SELECT a.name, ROUND(AVG(julianday(t.closed) - julianday(t.opened)), 2) AS avg_days
FROM agents a
JOIN tickets t ON t.agent_id = a.id AND t.closed IS NOT NULL
GROUP BY a.id, a.name
ORDER BY avg_days DESC;

-- Q3
SELECT name, id, days FROM (
  SELECT a.name, t.id,
         CAST(julianday(t.closed) - julianday(t.opened) AS INTEGER) AS days,
         ROW_NUMBER() OVER (PARTITION BY a.id
                            ORDER BY julianday(t.closed) - julianday(t.opened) DESC, t.id) AS rn
  FROM agents a
  JOIN tickets t ON t.agent_id = a.id AND t.closed IS NOT NULL
)
WHERE rn = 1
ORDER BY name;

-- Q4
SELECT a.name
FROM agents a
WHERE NOT EXISTS (
  SELECT 1 FROM tickets t
  WHERE t.agent_id = a.id AND t.priority = 'high'
    AND (t.closed IS NULL OR julianday(t.closed) - julianday(t.opened) > 2)
)
ORDER BY a.name;
