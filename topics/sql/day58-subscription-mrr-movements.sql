-- Day 58, Task 3 -- SQL: month-end MRR snapshots and an MRR movement (bridge) report.
--
-- Self-contained. Load with: sqlite3 practice_day58.db < day58-subscription-mrr-movements.sql
-- (needs window functions + recursive CTEs: SQLite >= 3.25, or PostgreSQL / MySQL 8).
--
-- THE PROBLEM
-- sub_events(event_id, customer_id, event_date, mrr) is a subscription change log:
-- each row says "from event_date on, this customer pays `mrr` per month" (a
-- cancellation is simply a row with mrr = 0). A customer's MRR ON a date d is the mrr of
-- their event with the latest event_date <= d (ties on the same date: highest
-- event_id wins); before their first event it is 0.
-- The reporting months are 2026-01 .. 2026-06; a month's snapshot is taken at the END
-- of that month (its last day). December 2025's month-end is the baseline for January.
-- Write 3 queries below the data. Nothing pre-solved.
--
-- Q1: month (as 'YYYY-MM'), total_mrr, paying_customers (mrr > 0) for every reporting
--     month, INCLUDING months with no events at all. Generate the months with a
--     RECURSIVE CTE (do not hard-code six rows). Order by month.
--     Hint: month-end = date(month_start, '+1 month', '-1 day') in SQLite.
-- Q2: The MRR bridge per reporting month. For every customer compare prev = MRR at the
--     previous month-end with cur = MRR at this month-end and classify the change:
--       new          prev = 0, cur > 0, and the customer had mrr = 0 at EVERY earlier
--                    month-end since the baseline (never paid at a snapshot before)
--       reactivation prev = 0, cur > 0, and the customer DID pay at some earlier
--                    month-end snapshot
--       expansion    prev > 0, cur > prev        contraction  prev > 0, 0 < cur < prev
--       churn        prev > 0, cur = 0
--     Output: month, new_mrr, expansion_mrr, contraction_mrr, churned_mrr,
--     reactivation_mrr, net_change -- contraction_mrr and churned_mrr as POSITIVE
--     amounts, net_change = new + expansion + reactivation - contraction - churned, which
--     must equal the change in Q1's total_mrr. All six months, 0 instead of NULL.
--     Note: a customer who starts and cancels inside one month never shows up.
-- Q3: Net revenue retention of the "January book": customers paying at 2026-01 month-end.
--     Output: jan_mrr (their MRR at Jan month-end), jun_mrr (THOSE SAME customers' MRR at
--     June month-end), nrr_pct = ROUND(100.0 * jun_mrr / jan_mrr, 1).
--
-- Expected results for the data below:
--   Q1: 2026-01|190|4   2026-02|250|5   2026-03|140|3
--       2026-04|140|3   2026-05|280|5   2026-06|240|5
--   Q2: month  |new|exp|contr|churn|react| net
--       2026-01|110|  0|   0 |   0 |   0 | 110
--       2026-02| 30| 30|   0 |   0 |   0 |  60
--       2026-03|  0|  0|   0 | 110 |   0 |-110
--       2026-04|  0|  0|   0 |   0 |   0 |   0
--       2026-05| 40| 60|   0 |   0 |  40 | 140
--       2026-06|  0|  0|  40 |   0 |   0 | -40
--   Q3: 190|170|89.5

CREATE TABLE sub_events (event_id INTEGER PRIMARY KEY, customer_id INTEGER,
                         event_date TEXT, mrr INTEGER);
INSERT INTO sub_events VALUES
 (1,  1, '2025-11-03', 50),   -- c1: steady, upgrades in Feb and May
 (2,  1, '2026-02-10', 80),
 (3,  1, '2026-05-01', 100),
 (4,  2, '2025-12-15', 30),   -- c2: steady 30
 (5,  3, '2026-01-20', 50),   -- c3: new in Jan, cancels in Mar, comes back in May
 (6,  3, '2026-03-05', 0),
 (7,  3, '2026-05-12', 40),
 (8,  4, '2026-02-01', 30),   -- c4: new in Feb, two changes on one day in Mar
 (9,  4, '2026-03-31', 0),
 (10, 4, '2026-03-31', 30),   --     (same day, higher id wins -> still 30)
 (11, 4, '2026-05-20', 70),   --     expands in May
 (12, 4, '2026-06-30', 30),   --     contracts on the last day of June
 (13, 5, '2026-04-02', 25),   -- c5: starts and cancels inside April -> invisible
 (14, 5, '2026-04-25', 0),
 (15, 6, '2026-05-31', 40),   -- c6: new on the last day of May
 (16, 7, '2026-01-10', 60),   -- c7: new in Jan, churns in Mar, never returns
 (17, 7, '2026-03-01', 0);

-- Q1
WITH RECURSIVE months(month_start) AS (
    SELECT '2026-01-01'
    UNION ALL
    SELECT date(month_start, '+1 month') FROM months WHERE month_start < '2026-06-01'
),
month_ends AS (
    SELECT strftime('%Y-%m', month_start) AS month,
           date(month_start, '+1 month', '-1 day') AS month_end
    FROM months
),
customers AS (SELECT DISTINCT customer_id FROM sub_events),
snapshots AS (
    SELECT me.month, c.customer_id,
           COALESCE((SELECT e.mrr FROM sub_events e
                     WHERE e.customer_id = c.customer_id AND e.event_date <= me.month_end
                     ORDER BY e.event_date DESC, e.event_id DESC
                     LIMIT 1), 0) AS mrr
    FROM month_ends me CROSS JOIN customers c
)
SELECT month,
       SUM(mrr)     AS total_mrr,
       SUM(mrr > 0) AS paying_customers
FROM snapshots
GROUP BY month
ORDER BY month;

-- Q2
WITH RECURSIVE months(month_start) AS (
    SELECT '2025-12-01'                 -- baseline month-end (Dec 2025) + the 6 reporting months
    UNION ALL
    SELECT date(month_start, '+1 month') FROM months WHERE month_start < '2026-06-01'
),
month_ends AS (
    SELECT strftime('%Y-%m', month_start) AS month,
           date(month_start, '+1 month', '-1 day') AS month_end
    FROM months
),
customers AS (SELECT DISTINCT customer_id FROM sub_events),
snapshots AS (
    SELECT me.month, c.customer_id,
           COALESCE((SELECT e.mrr FROM sub_events e
                     WHERE e.customer_id = c.customer_id AND e.event_date <= me.month_end
                     ORDER BY e.event_date DESC, e.event_id DESC
                     LIMIT 1), 0) AS mrr
    FROM month_ends me CROSS JOIN customers c
),
compared AS (
    SELECT month, customer_id, mrr AS cur,
           LAG(mrr) OVER w AS prev,
           -- highest MRR at any month-end snapshot BEFORE this one (baseline included)
           MAX(mrr) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS max_before
    FROM snapshots
    WINDOW w AS (PARTITION BY customer_id ORDER BY month)
),
classified AS (
    SELECT month, cur, prev,
           CASE
               WHEN prev = 0 AND cur > 0 AND max_before = 0 THEN 'new'
               WHEN prev = 0 AND cur > 0                    THEN 'reactivation'
               WHEN prev > 0 AND cur > prev                 THEN 'expansion'
               WHEN prev > 0 AND cur > 0 AND cur < prev     THEN 'contraction'
               WHEN prev > 0 AND cur = 0                    THEN 'churn'
           END AS kind
    FROM compared
    WHERE month > '2025-12'                     -- the baseline itself is not reported
),
bridge AS (
    SELECT month,
           SUM(CASE WHEN kind = 'new'          THEN cur - prev ELSE 0 END) AS new_mrr,
           SUM(CASE WHEN kind = 'expansion'    THEN cur - prev ELSE 0 END) AS expansion_mrr,
           SUM(CASE WHEN kind = 'contraction'  THEN prev - cur ELSE 0 END) AS contraction_mrr,
           SUM(CASE WHEN kind = 'churn'        THEN prev       ELSE 0 END) AS churned_mrr,
           SUM(CASE WHEN kind = 'reactivation' THEN cur        ELSE 0 END) AS reactivation_mrr
    FROM classified
    GROUP BY month
)
SELECT month, new_mrr, expansion_mrr, contraction_mrr, churned_mrr, reactivation_mrr,
       new_mrr + expansion_mrr + reactivation_mrr - contraction_mrr - churned_mrr AS net_change
FROM bridge
ORDER BY month;

-- Q3
WITH snap(customer_id, jan, jun) AS (
    SELECT c.customer_id,
           COALESCE((SELECT e.mrr FROM sub_events e
                     WHERE e.customer_id = c.customer_id AND e.event_date <= '2026-01-31'
                     ORDER BY e.event_date DESC, e.event_id DESC LIMIT 1), 0),
           COALESCE((SELECT e.mrr FROM sub_events e
                     WHERE e.customer_id = c.customer_id AND e.event_date <= '2026-06-30'
                     ORDER BY e.event_date DESC, e.event_id DESC LIMIT 1), 0)
    FROM (SELECT DISTINCT customer_id FROM sub_events) c
),
jan_book AS (SELECT * FROM snap WHERE jan > 0)   -- customers paying at Jan month-end
SELECT SUM(jan) AS jan_mrr,
       SUM(jun) AS jun_mrr,
       ROUND(100.0 * SUM(jun) / SUM(jan), 1) AS nrr_pct
FROM jan_book;

