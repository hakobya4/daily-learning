-- Day 10, Task 1 -- SQL: gaps and islands.
--
-- Self-contained. Load with: sqlite3 practice_day10.db < day10-gaps-and-islands.sql
--
-- THE PROBLEM
-- login_days holds one row per (user, day) on which the user logged in.
-- Write 3 queries. Nothing is pre-solved.
--
-- Q1: For each user, list every "streak" (island) of consecutive days:
--     user_id, streak_start, streak_end, streak_len. Order by user_id,
--     streak_start.
-- Q2: For each user, the length of their LONGEST streak (user_id,
--     best_streak). Order by user_id.
-- Q3: Users whose longest streak is >= 3 days, with the date it ended.
--
-- HINT: for consecutive days, (day - ROW_NUMBER() OVER (PARTITION BY
-- user_id ORDER BY day)) is constant within a streak. In SQLite use
-- julianday(day) - ROW_NUMBER() ... and GROUP BY that value.

DROP TABLE IF EXISTS login_days;
CREATE TABLE login_days (
    user_id INTEGER NOT NULL,
    day     TEXT NOT NULL      -- 'YYYY-MM-DD'
);
INSERT INTO login_days (user_id, day) VALUES
    (1, '2026-09-01'), (1, '2026-09-02'), (1, '2026-09-03'),
    (1, '2026-09-07'), (1, '2026-09-08'),
    (2, '2026-09-01'), (2, '2026-09-03'), (2, '2026-09-05'),
    (3, '2026-09-10'), (3, '2026-09-11'), (3, '2026-09-12'), (3, '2026-09-13'),
    (3, '2026-09-20');

-- Q1: every streak per user
SELECT user_id,
       MIN(day) AS streak_start,
       MAX(day) AS streak_end,
       COUNT(*) AS streak_len
FROM (
    SELECT user_id, day,
           julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
    FROM login_days
)
GROUP BY user_id, grp
ORDER BY user_id, streak_start;

-- Q2: longest streak per user
WITH streaks AS (
    SELECT user_id,
           MIN(day) AS streak_start,
           MAX(day) AS streak_end,
           COUNT(*) AS streak_len
    FROM (
        SELECT user_id, day,
               julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
        FROM login_days
    )
    GROUP BY user_id, grp
)
SELECT user_id, MAX(streak_len) AS best_streak
FROM streaks
GROUP BY user_id
ORDER BY user_id;

-- Q3: users whose longest streak is >= 3 days, with the date it ended
WITH streaks AS (
    SELECT user_id,
           MIN(day) AS streak_start,
           MAX(day) AS streak_end,
           COUNT(*) AS streak_len
    FROM (
        SELECT user_id, day,
               julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
        FROM login_days
    )
    GROUP BY user_id, grp
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY streak_len DESC, streak_end) AS rn
    FROM streaks
)
SELECT user_id, streak_len AS best_streak, streak_end
FROM ranked
WHERE rn = 1 AND streak_len >= 3
ORDER BY user_id;
