-- Day 62, Task 3 -- SQL: project scheduling over a dependency DAG (recursive CTEs, critical path, slack).
--
-- Self-contained. Load with: sqlite3 practice_day62.db < day62-critical-path-schedule.sql
-- (SQLite >= 3.25 is plenty; only recursive CTEs and aggregates are needed.)
-- No sqlite3 CLI? python3 -c "import sqlite3; ..." runs it just as well.
--
-- THE PROBLEM
-- tasks(task_id, name, duration)  and  deps(task_id, depends_on)
-- A row in deps means: task_id may only START after depends_on has FINISHED.
-- The graph is acyclic. Day 0 is the project start; all tasks can run in parallel
-- as long as their prerequisites are done, and nothing waits longer than it must.
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Earliest schedule: name, es (earliest start), ef (earliest finish = es + duration),
--     one row per task, ordered by es, name.
--     es = 0 for a task with no prerequisites, otherwise the MAX ef over its
--     prerequisites. Hint: a recursive CTE that walks every path from the root tasks
--     (those with no row in deps as task_id) and accumulates finish times; then take
--     MAX per task. (Path enumeration is fine for a small DAG.)
-- Q2: Critical path and slack: name, es, ls, slack, critical -- ordered by slack, es, name.
--     project_end = MAX(ef) over all tasks.
--     ls (latest start) = project_end - duration for a task nothing depends on,
--     otherwise MIN(ls of the tasks that depend on it) - duration.
--     slack = ls - es; critical = 'Y' when slack = 0 else 'N'.
--     Hint: a SECOND recursive CTE that walks the edges BACKWARDS from the sink tasks.
-- Q3: Transitive prerequisites: name, n_prereqs = how many DISTINCT tasks must be
--     finished (directly or indirectly) before this task can start. Every task
--     appears, including those with 0. Ordered by n_prereqs DESC, name.
--     Hint: recursive closure with UNION (not UNION ALL) so each (task, prerequisite)
--     pair appears once -- spec is reachable from release along several paths.
--
-- Expected results for the data below:
--   Q1: logo|0|2
--       spec|0|3
--       design_db|3|7
--       design_ui|3|5
--       build_ui|5|10
--       build_api|7|13
--       seed_data|7|8
--       docs|13|15
--       integrate|13|16
--       qa|16|20
--       release|20|21
--   Q2: spec|0|0|0|Y
--       design_db|3|3|0|Y
--       build_api|7|7|0|Y
--       integrate|13|13|0|Y
--       qa|16|16|0|Y
--       release|20|20|0|Y
--       design_ui|3|6|3|N
--       build_ui|5|8|3|N
--       seed_data|7|12|5|N
--       docs|13|18|5|N
--       logo|0|18|18|N
--   Q3: release|10
--       qa|7
--       integrate|6
--       docs|3
--       build_api|2
--       build_ui|2
--       seed_data|2
--       design_db|1
--       design_ui|1
--       logo|0
--       spec|0

DROP TABLE IF EXISTS deps;
DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
  task_id  INTEGER PRIMARY KEY,
  name     TEXT    NOT NULL UNIQUE,
  duration INTEGER NOT NULL CHECK (duration > 0)   -- working days
);

CREATE TABLE deps (
  task_id    INTEGER NOT NULL REFERENCES tasks(task_id),  -- this task ...
  depends_on INTEGER NOT NULL REFERENCES tasks(task_id),  -- ... cannot start before this one finishes
  PRIMARY KEY (task_id, depends_on)
);

INSERT INTO tasks (task_id, name, duration) VALUES
 (1,  'spec',       3),
 (2,  'design_db',  4),
 (3,  'design_ui',  2),
 (4,  'build_api',  6),
 (5,  'build_ui',   5),
 (6,  'seed_data',  1),
 (7,  'integrate',  3),
 (8,  'docs',       2),
 (9,  'qa',         4),
 (10, 'release',    1),
 (11, 'logo',       2);

INSERT INTO deps (task_id, depends_on) VALUES
 (2, 1), (3, 1),
 (4, 2),
 (5, 3),
 (6, 2),
 (7, 4), (7, 5), (7, 6),
 (8, 4),
 (9, 7), (9, 1),
 (10, 9), (10, 8), (10, 11);

-- Q1: earliest start / earliest finish
WITH RECURSIVE paths(task_id, ef) AS (
  -- roots: tasks with no prerequisites start at day 0
  SELECT t.task_id, t.duration
  FROM tasks t
  WHERE NOT EXISTS (SELECT 1 FROM deps d WHERE d.task_id = t.task_id)
  UNION ALL
  -- extend every path one edge forward: successor finishes after its predecessor
  SELECT d.task_id, p.ef + t.duration
  FROM paths p
  JOIN deps d  ON d.depends_on = p.task_id
  JOIN tasks t ON t.task_id = d.task_id
),
early AS (
  SELECT task_id, MAX(ef) AS ef FROM paths GROUP BY task_id
)
SELECT t.name, e.ef - t.duration AS es, e.ef
FROM early e JOIN tasks t ON t.task_id = e.task_id
ORDER BY es, t.name;


-- Q2: latest start, slack and the critical path
WITH RECURSIVE paths(task_id, ef) AS (
  SELECT t.task_id, t.duration
  FROM tasks t
  WHERE NOT EXISTS (SELECT 1 FROM deps d WHERE d.task_id = t.task_id)
  UNION ALL
  SELECT d.task_id, p.ef + t.duration
  FROM paths p
  JOIN deps d  ON d.depends_on = p.task_id
  JOIN tasks t ON t.task_id = d.task_id
),
early AS (
  SELECT task_id, MAX(ef) AS ef FROM paths GROUP BY task_id
),
proj AS (
  SELECT MAX(ef) AS project_end FROM early
),
back(task_id, ls) AS (
  -- sinks: nothing depends on them, so they may start as late as end - duration
  SELECT t.task_id, (SELECT project_end FROM proj) - t.duration
  FROM tasks t
  WHERE NOT EXISTS (SELECT 1 FROM deps d WHERE d.depends_on = t.task_id)
  UNION ALL
  -- walk edges backwards: a prerequisite must finish before its dependent's start
  SELECT d.depends_on, b.ls - t.duration
  FROM back b
  JOIN deps d  ON d.task_id = b.task_id
  JOIN tasks t ON t.task_id = d.depends_on
),
late AS (
  SELECT task_id, MIN(ls) AS ls FROM back GROUP BY task_id
)
SELECT t.name,
       e.ef - t.duration                      AS es,
       l.ls,
       l.ls - (e.ef - t.duration)             AS slack,
       CASE WHEN l.ls = e.ef - t.duration THEN 'Y' ELSE 'N' END AS critical
FROM tasks t
JOIN early e ON e.task_id = t.task_id
JOIN late  l ON l.task_id = t.task_id
ORDER BY slack, es, t.name;


-- Q3: number of distinct transitive prerequisites per task
WITH RECURSIVE closure(task_id, prereq) AS (
  SELECT task_id, depends_on FROM deps
  UNION                                   -- UNION de-duplicates (task, prereq) pairs
  SELECT c.task_id, d.depends_on
  FROM closure c
  JOIN deps d ON d.task_id = c.prereq
)
SELECT t.name, COUNT(c.prereq) AS n_prereqs
FROM tasks t
LEFT JOIN closure c ON c.task_id = t.task_id
GROUP BY t.task_id, t.name
ORDER BY n_prereqs DESC, t.name;
