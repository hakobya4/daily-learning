-- Day 15, Task 1 -- SQL: CUME_DIST/PERCENT_RANK, subtotals with UNION ALL, running distinct-ish counts.
--
-- Self-contained. Load with: sqlite3 practice_day15.db < day15-cume-dist-and-subtotals.sql
--
-- THE PROBLEM
-- scores(id, student, course, score). Write 5 queries. Nothing is pre-solved.
--
-- Q1: Percentile standing within each course: (course, student, score,
--     pct_rank, cume) with PERCENT_RANK() and CUME_DIST() OVER
--     (PARTITION BY course ORDER BY score), both rounded to 2 decimals.
--     Order by course, score, student.
-- Q2: Students whose CUME_DIST in their course is >= 0.75 (the top
--     quarter, ties included): (course, student, score). Hint: CTE.
-- Q3: Subtotal report with UNION ALL (SQLite has no ROLLUP): one row per
--     course with its average score (1 decimal), plus a final 'ALL'
--     grand-total row: (course, avg_score). Order courses alphabetically,
--     'ALL' last.
-- Q4: Each student's average across courses and how it compares with the
--     overall average of student averages: (student, avg_score, diff)
--     rounded to 1 decimal. Order by diff DESC, student.
-- Q5: Running count of students who have scored >= 80 so far, ordered
--     by id: (id, student, score, running_high). Use SUM(CASE ...) OVER
--     (ORDER BY id).

DROP TABLE IF EXISTS scores;
CREATE TABLE scores (
    id      INTEGER PRIMARY KEY,
    student TEXT NOT NULL,
    course  TEXT NOT NULL,
    score   INTEGER NOT NULL
);
INSERT INTO scores (id, student, course, score) VALUES
 (1,'Ana','SQL',92),(2,'Ben','SQL',75),(3,'Cy','SQL',75),(4,'Dee','SQL',60),
 (5,'Ana','PY',81),(6,'Ben','PY',88),(7,'Cy','PY',54),(8,'Dee','PY',88),
 (9,'Ana','UNIX',70),(10,'Ben','UNIX',95),(11,'Cy','UNIX',82),(12,'Dee','UNIX',49);

-- Q1
-- TODO

-- Q2
-- TODO

-- Q3
-- TODO

-- Q4
-- TODO

-- Q5
-- TODO
