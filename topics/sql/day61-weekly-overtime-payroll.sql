-- Day 61, Task 3 -- SQL: weekly overtime from daily timesheets (ISO weeks, LAG, conditional pay).
--
-- Self-contained. Load with: sqlite3 practice_day61.db < day61-weekly-overtime-payroll.sql
-- (SQLite >= 3.25 for window functions.)
-- No sqlite3 CLI? python3 -c "import sqlite3; ..." runs it just as well.
--
-- THE PROBLEM
-- employees(emp_id, name, hourly_rate)  and  timesheets(emp_id, work_date, hours)
-- work_date is 'YYYY-MM-DD'. An employee can have MORE THAN ONE row for the same day
-- (a split shift) -- they simply add up.
-- Work weeks run MONDAY .. SUNDAY and are identified by their Monday (week_start).
-- Overtime rule: hours above 40 in a work week are overtime and are paid at 1.5x the
-- hourly rate; the first 40 hours of a week are regular. Overtime is computed PER WEEK,
-- never per day and never over the whole period.
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: Weekly totals: name, week_start, total_hours, overtime_hours (0 when <= 40),
--     one row per employee per week they worked, ordered by week_start, name.
--     Hint: date(work_date, 'weekday 0', '-6 days') maps any date to the Monday of its
--     Mon..Sun week ('weekday 0' moves FORWARD to the next Sunday, or stays on a Sunday).
--     Check that Sunday 2026-11-08 lands in the week of 2026-11-02, not 2026-11-09.
-- Q2: Payroll for the whole period: name, regular_hours, overtime_hours,
--     total_pay = regular_hours * rate + overtime_hours * rate * 1.5 (ROUND to 2),
--     and pay_rank (DENSE_RANK over total_pay, highest = 1). Ordered by pay_rank, name.
--     Hint: aggregate per week FIRST (a CTE), then sum MIN(total, 40) and
--     MAX(total - 40, 0) per employee -- the scalar two-argument MIN/MAX, not aggregates.
-- Q3: Week-over-week jumps: name, week_start, prev_hours, hours, increase -- rows where
--     an employee worked MORE hours than in the IMMEDIATELY preceding calendar week.
--     If the employee did not work at all in the preceding week, the row does not
--     qualify (use LAG on both hours and week_start and require
--     prev_week_start = date(week_start, '-7 days')). Ordered by week_start, name.
--
-- Expected results for the data below (4 vs 4.0 display differences don't matter):
--   Q1: Ani|2026-11-02|44.0|4.0
--       Davit|2026-11-02|24.0|0
--       Lilit|2026-11-02|45.0|5.0
--       Ani|2026-11-09|32.0|0
--       Davit|2026-11-09|46.0|6.0
--       Lilit|2026-11-09|37.5|0
--       Tigran|2026-11-09|12.0|0
--       Ani|2026-11-16|44.0|4.0
--       Davit|2026-11-16|8.0|0
--       Tigran|2026-11-16|47.0|7.0
--   Q2: Ani|112.0|8.0|3720.0|1
--       Lilit|77.5|5.0|3400.0|2
--       Davit|72.0|6.0|2025.0|3
--       Tigran|52.0|7.0|1250.0|4
--   Q3: Davit|2026-11-09|24.0|46.0|22.0
--       Ani|2026-11-16|32.0|44.0|12.0
--       Tigran|2026-11-16|12.0|47.0|35.0

CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, name TEXT, hourly_rate REAL);
INSERT INTO employees VALUES
 (1, 'Ani', 30.0), (2, 'Davit', 25.0), (3, 'Lilit', 40.0), (4, 'Tigran', 20.0);

CREATE TABLE timesheets (emp_id INTEGER REFERENCES employees(emp_id), work_date TEXT, hours REAL);
INSERT INTO timesheets VALUES
 -- week of Mon 2026-11-02
 (1, '2026-11-02', 9), (1, '2026-11-03', 9), (1, '2026-11-04', 9), (1, '2026-11-05', 9), (1, '2026-11-06', 8),
 (2, '2026-11-02', 8), (2, '2026-11-03', 8), (2, '2026-11-04', 8),
 (3, '2026-11-03', 10), (3, '2026-11-04', 10), (3, '2026-11-05', 10), (3, '2026-11-06', 10), (3, '2026-11-08', 5),
 -- week of Mon 2026-11-09
 (1, '2026-11-09', 8), (1, '2026-11-10', 8), (1, '2026-11-11', 8), (1, '2026-11-12', 8),
 (2, '2026-11-09', 10), (2, '2026-11-10', 10), (2, '2026-11-11', 10), (2, '2026-11-12', 10), (2, '2026-11-14', 6),
 (3, '2026-11-09', 7.5), (3, '2026-11-10', 7.5), (3, '2026-11-11', 7.5), (3, '2026-11-12', 7.5), (3, '2026-11-13', 7.5),
 (4, '2026-11-15', 12),
 -- week of Mon 2026-11-16
 (1, '2026-11-16', 11), (1, '2026-11-17', 11), (1, '2026-11-18', 11), (1, '2026-11-19', 11),
 (2, '2026-11-16', 8),
 (4, '2026-11-16', 9), (4, '2026-11-17', 9), (4, '2026-11-18', 9), (4, '2026-11-19', 9), (4, '2026-11-20', 9),
 (4, '2026-11-17', 2);

-- Q1: weekly totals and overtime
-- TODO: write your query here


-- Q2: payroll with 1.5x overtime and DENSE_RANK
-- TODO: write your query here


-- Q3: week-over-week increases (consecutive weeks only)
-- TODO: write your query here
