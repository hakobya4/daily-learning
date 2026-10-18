-- Day 28, Task 1 -- SQL: gaps and islands, ROW_NUMBER difference trick.
--
-- Self-contained. Load with: sqlite3 practice_day28.db < day28-gaps-and-islands.sql
--
-- THE PROBLEM
-- attendance has one row per (student, day number) the student was present.
-- Write 3 queries. Nothing pre-solved.
--
-- Q1: "Islands": for each student, every run of consecutive days present:
--     student, start_day, end_day, run_length. Order by student, start_day.
-- Q2: The longest run per student: student, run_length (ties: earliest
--     start_day only). Order by student.
-- Q3: "Gaps": for each student, the missing day ranges BETWEEN their first
--     and last present day: student, gap_start, gap_end. Order by student,
--     gap_start.
--
-- HINT: day - ROW_NUMBER() OVER (PARTITION BY student ORDER BY day) is
-- constant within an island; GROUP BY it. For gaps use LEAD(day) and keep
-- rows where next_day - day > 1 (gap = day+1 .. next_day-1).

DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
    student TEXT    NOT NULL,
    day     INTEGER NOT NULL,
    PRIMARY KEY (student, day)
);
INSERT INTO attendance (student, day) VALUES
    ('ana', 1), ('ana', 2), ('ana', 3), ('ana', 6), ('ana', 7), ('ana', 10),
    ('ben', 4), ('ben', 5), ('ben', 6), ('ben', 7),
    ('cy',  1), ('cy',  3), ('cy',  5);

-- Q1: islands
SELECT student, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS run_length
FROM (
    SELECT student, day,
           day - ROW_NUMBER() OVER (PARTITION BY student ORDER BY day) AS grp
    FROM attendance
)
GROUP BY student, grp
ORDER BY student, start_day;

-- Q2: longest run per student
WITH islands AS (
    SELECT student, MIN(day) AS start_day, COUNT(*) AS run_length
    FROM (
        SELECT student, day,
               day - ROW_NUMBER() OVER (PARTITION BY student ORDER BY day) AS grp
        FROM attendance
    )
    GROUP BY student, grp
),
ranked AS (
    SELECT student, run_length,
           ROW_NUMBER() OVER (PARTITION BY student ORDER BY run_length DESC, start_day) AS rn
    FROM islands
)
SELECT student, run_length FROM ranked WHERE rn = 1 ORDER BY student;

-- Q3: gaps
SELECT student, day + 1 AS gap_start, next_day - 1 AS gap_end
FROM (
    SELECT student, day,
           LEAD(day) OVER (PARTITION BY student ORDER BY day) AS next_day
    FROM attendance
)
WHERE next_day - day > 1
ORDER BY student, gap_start;
