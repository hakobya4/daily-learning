-- Day 4, Task 2 -- SQL: correlated subqueries and EXISTS.
--
-- Self-contained: schema + data + queries all in this one file
-- (unlike Task 1, there's no separate schema file for this one).
-- Load it with: sqlite3 practice_day4b.db < day4-correlated-subqueries.sql
--
-- Nothing below is pre-solved. Write each query yourself.

DROP TABLE IF EXISTS enrollments_sql;
DROP TABLE IF EXISTS courses_sql;
DROP TABLE IF EXISTS students_sql;

CREATE TABLE students_sql (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE courses_sql (
    id         INTEGER PRIMARY KEY,
    title      TEXT NOT NULL,
    department TEXT NOT NULL
);

CREATE TABLE enrollments_sql (
    student_id INTEGER REFERENCES students_sql(id),
    course_id  INTEGER REFERENCES courses_sql(id),
    grade      REAL NOT NULL
);

INSERT INTO students_sql (id, name) VALUES
    (1, 'Maria'),
    (2, 'Noah'),
    (3, 'Olivia'),
    (4, 'Liam'),
    (5, 'Emma');

INSERT INTO courses_sql (id, title, department) VALUES
    (1, 'Intro to CS',      'Computer Science'),
    (2, 'Data Structures',  'Computer Science'),
    (3, 'Calculus I',       'Math'),
    (4, 'Art History',      'Humanities');

INSERT INTO enrollments_sql (student_id, course_id, grade) VALUES
    (1, 1, 85),
    (1, 3, 78),
    (2, 1, 91),
    (2, 2, 88),
    (3, 3, 95),
    (3, 4, 82),
    (4, 4, 70);
-- note: Emma (id 5) has no enrollments at all -- that's deliberate,
-- for Q2.

-- Q1: List the names of students enrolled in AT LEAST ONE 'Computer
-- Science' course (join courses_sql via enrollments_sql). Do this
-- with an EXISTS correlated subquery, not a JOIN + DISTINCT.
SELECT s.name
FROM students_sql s
WHERE EXISTS (
    SELECT 1
    FROM enrollments_sql e
    JOIN courses_sql c ON c.id = e.course_id
    WHERE e.student_id = s.id
      AND c.department = 'Computer Science'
);


-- Q2: List the names of students who are NOT enrolled in ANY course
-- at all. Day 2's Q3 solved a similar shape with a LEFT JOIN ...
-- WHERE ... IS NULL antipattern -- do THIS one with a NOT EXISTS
-- correlated subquery instead, for comparison.
SELECT s.name
FROM students_sql s
WHERE NOT EXISTS (
    SELECT 1
    FROM enrollments_sql e
    WHERE e.student_id = s.id
);


-- Q3: For each course, list the students whose grade is HIGHER than
-- the AVERAGE grade in that SAME course. The average has to be
-- recomputed per course, so the subquery needs to reference the
-- outer query's course_id (a correlated subquery, not a plain one).
SELECT c.title, s.name, e.grade
FROM enrollments_sql e
JOIN students_sql s ON s.id = e.student_id
JOIN courses_sql c ON c.id = e.course_id
WHERE e.grade > (
    SELECT AVG(e2.grade)
    FROM enrollments_sql e2
    WHERE e2.course_id = e.course_id
);
