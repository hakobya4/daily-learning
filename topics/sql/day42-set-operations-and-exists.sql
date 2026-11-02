-- Day 42, Task 6 -- SQL: set operations, EXISTS and anti-joins.
--
-- Self-contained. Load with: sqlite3 practice_day42.db < day42-set-operations-and-exists.sql
--
-- THE PROBLEM
-- students(id, name), courses(id, title), enrolled(student_id, course_id).
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Students enrolled in NO course (use NOT EXISTS). Output: name. Order by name.
-- Q2: Students enrolled in BOTH 'SQL' and 'Python' (use INTERSECT on the
--     two sets of student names). Output: name. Order by name.
-- Q3: Students enrolled in 'SQL' but NOT in 'Python' (use EXCEPT).
--     Output: name. Order by name.
--
-- Expected results for the data below:
--   Q1: dee
--   Q2: ann
--   Q3: bo

CREATE TABLE students (id INTEGER, name TEXT);
CREATE TABLE courses  (id INTEGER, title TEXT);
CREATE TABLE enrolled (student_id INTEGER, course_id INTEGER);
INSERT INTO students VALUES (1,'ann'),(2,'bo'),(3,'cy'),(4,'dee');
INSERT INTO courses  VALUES (1,'SQL'),(2,'Python'),(3,'Unix');
INSERT INTO enrolled VALUES (1,1),(1,2),(2,1),(3,2),(3,3);

-- Q1
SELECT s.name
FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrolled e WHERE e.student_id = s.id)
ORDER BY s.name;

-- Q2
SELECT name FROM (
  SELECT s.name FROM students s
  JOIN enrolled e ON e.student_id = s.id
  JOIN courses c ON c.id = e.course_id WHERE c.title = 'SQL'
  INTERSECT
  SELECT s.name FROM students s
  JOIN enrolled e ON e.student_id = s.id
  JOIN courses c ON c.id = e.course_id WHERE c.title = 'Python'
)
ORDER BY name;

-- Q3
SELECT name FROM (
  SELECT s.name FROM students s
  JOIN enrolled e ON e.student_id = s.id
  JOIN courses c ON c.id = e.course_id WHERE c.title = 'SQL'
  EXCEPT
  SELECT s.name FROM students s
  JOIN enrolled e ON e.student_id = s.id
  JOIN courses c ON c.id = e.course_id WHERE c.title = 'Python'
)
ORDER BY name;
