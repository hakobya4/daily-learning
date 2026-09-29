-- Day 9, Task 1 -- SQL: ranking with ties (RANK vs DENSE_RANK vs ROW_NUMBER, NTILE).
--
-- Self-contained: schema + data + queries. Load with:
--   sqlite3 practice_day9a.db < day9-ranking-ties.sql
-- (needs SQLite 3.25+ for window functions)
--
-- THE PROBLEM
-- Write 3 queries against scores_sql. Nothing below is pre-solved.
--
-- Q1: For every row show player, game, points and RANK() within each
--     game (highest points = rank 1). Order by game, rank, player.
-- Q2: Same, but add DENSE_RANK() as a second column next to RANK() so
--     you can SEE where they differ on ties. Order by game, player.
-- Q3: Split ALL rows into 3 equal-ish buckets by points (highest
--     bucket = 1) using NTILE(3) OVER (ORDER BY points DESC, player);
--     show player, points, bucket.
--
-- HINT: RANK leaves gaps after ties (1,1,3), DENSE_RANK doesn't (1,1,2).

DROP TABLE IF EXISTS scores_sql;
CREATE TABLE scores_sql (
    id     INTEGER PRIMARY KEY,
    player TEXT NOT NULL,
    game   TEXT NOT NULL,
    points INTEGER NOT NULL
);
INSERT INTO scores_sql (id, player, game, points) VALUES
    (1, 'Ari',  'chess', 90),
    (2, 'Bo',   'chess', 90),
    (3, 'Cy',   'chess', 75),
    (4, 'Di',   'chess', 60),
    (5, 'Ari',  'go',    88),
    (6, 'Cy',   'go',    88),
    (7, 'Di',   'go',    88),
    (8, 'Bo',   'go',    70);

-- Q1: TODO: write this query


-- Q2: TODO: write this query


-- Q3: TODO: write this query

