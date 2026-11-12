-- Day 53, Task 6 -- SQL: bill-of-materials explosion with a recursive CTE.
--
-- Self-contained. Load with: sqlite3 practice_day53.db < day53-bom-explosion.sql
--
-- THE PROBLEM
-- bom(parent, child, qty) -- one `parent` contains `qty` units of `child`. A child can itself
-- be a parent (sub-assembly). A part that is never a parent is a LEAF (raw part).
-- leaf_cost(part, unit_cost) -- price of one unit of each leaf part.
-- The same part (bolt) appears under several sub-assemblies -- quantities MULTIPLY down a
-- path and ADD UP across paths. Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Explode 'bike': one row per (path step) with depth (1 = direct child of bike), the
--     immediate parent, the part, and qty_per_bike = product of qty along the path.
--     Output: depth, parent, part, qty_per_bike. Order by depth, parent, part.
--     Hint: WITH RECURSIVE x(depth, parent, part, qty) AS (anchor: bom rows WHERE parent =
--     'bike'; recursive step: JOIN bom ON bom.parent = x.part, qty = x.qty * bom.qty).
-- Q2: Total units of each LEAF part needed to build ONE bike. Output: part, total_qty.
--     Order by part. Hint: leaf = NOT EXISTS (SELECT 1 FROM bom WHERE parent = part).
-- Q3: Total raw-material cost of one bike. Output: one column bike_cost.
-- Q4: For each DIRECT child of bike, how many DISTINCT leaf parts it contains (anywhere
--     below it). Output: assembly, distinct_leaves. Order by assembly.
--     Hint: start the recursion per direct child and carry the root assembly along.
--
-- Expected results for the data below:
--   Q1: 1|bike|frame|1   1|bike|seat|1    1|bike|wheel|2
--       2|frame|bolt|4   2|frame|tube|3   2|seat|bolt|1   2|seat|cushion|1
--       2|wheel|bolt|4   2|wheel|hub|2    2|wheel|rim|2   2|wheel|spoke|64
--       3|hub|axle|2     3|hub|bearing|4
--   Q2: axle|2  bearing|4  bolt|9  cushion|1  rim|2  spoke|64  tube|3
--   Q3: 250
--   Q4: frame|2  seat|2  wheel|5

CREATE TABLE bom (parent TEXT, child TEXT, qty INTEGER);
INSERT INTO bom VALUES
 ('bike','frame',1),
 ('bike','wheel',2),
 ('bike','seat',1),
 ('frame','tube',3),
 ('frame','bolt',4),
 ('wheel','spoke',32),
 ('wheel','rim',1),
 ('wheel','bolt',2),
 ('wheel','hub',1),
 ('hub','axle',1),
 ('hub','bearing',2),
 ('seat','bolt',1),
 ('seat','cushion',1);

CREATE TABLE leaf_cost (part TEXT, unit_cost INTEGER);
INSERT INTO leaf_cost VALUES
 ('tube',12),('bolt',1),('spoke',2),('rim',20),('cushion',15),('axle',5),('bearing',3);

-- Q1
-- TODO: your query here

-- Q2
-- TODO: your query here

-- Q3
-- TODO: your query here

-- Q4
-- TODO: your query here
