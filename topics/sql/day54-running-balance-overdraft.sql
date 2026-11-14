-- Day 54, Task 6 -- SQL: running balances, first overdraft, max drawdown, negative streaks.
--
-- Self-contained. Load with: sqlite3 practice_day54.db < day54-running-balance-overdraft.sql
-- (needs window functions: SQLite >= 3.25, or any PostgreSQL / MySQL 8).
--
-- THE PROBLEM
-- accounts(account, opening_balance) -- balance before the first transaction.
-- txn(id, account, txn_date, amount) -- positive = deposit, negative = withdrawal.
-- Transactions are applied in order of (txn_date, id); several can share a date.
-- Write 4 queries below the data. Nothing pre-solved.
--
-- Q1: Balance after every transaction. Output: account, txn_date, amount, balance.
--     Order by account, txn_date, id.
--     Hint: opening_balance + SUM(amount) OVER (PARTITION BY account ORDER BY txn_date, id).
--     Careful: with only ORDER BY txn_date, two rows on the same date would get the SAME
--     running sum (default RANGE frame treats ties as peers) -- include id in the ORDER BY.
-- Q2: For each account that EVER went below zero, the first date its balance was negative.
--     Output: account, first_overdraft. Order by account.
-- Q3: Maximum drawdown per account: the largest drop from a previous peak balance to a later
--     balance. The opening balance counts as the initial peak. Accounts that never dropped
--     show 0. Output: account, max_drawdown. Order by account.
--     Hint: peak_so_far = MAX(opening_balance, running MAX(balance) OVER (...)); then
--     MAX(peak_so_far - balance) per account. (SQLite's 2-arg MAX(a, b) is scalar
--     "greatest"; in PostgreSQL use GREATEST.)
-- Q4: Longest run of CONSECUTIVE transactions (in apply order) after which the balance was
--     negative. Accounts that never went negative show 0. Output: account,
--     longest_negative_streak. Order by account.
--     Hint: gaps-and-islands -- ROW_NUMBER() over all rows minus ROW_NUMBER() partitioned
--     also by (balance < 0) is constant inside each run.
--
-- Expected results for the data below:
--   Q1: A|2026-11-01|-30|70    A|2026-11-02|-90|-20   A|2026-11-02|50|30
--       A|2026-11-04|-40|-10   A|2026-11-05|-10|-20   A|2026-11-07|100|80
--       B|2026-11-01|200|200   B|2026-11-03|-50|150   B|2026-11-06|-25|125
--       C|2026-11-02|-60|-10   C|2026-11-03|20|10     C|2026-11-05|-30|-20
--       C|2026-11-08|-10|-30   C|2026-11-09|90|60
--   Q2: A|2026-11-02   C|2026-11-02
--   Q3: A|120   B|75   C|80
--   Q4: A|2   B|0   C|2

CREATE TABLE accounts (account TEXT PRIMARY KEY, opening_balance INTEGER);
INSERT INTO accounts VALUES ('A', 100), ('B', 0), ('C', 50);

CREATE TABLE txn (id INTEGER PRIMARY KEY, account TEXT, txn_date TEXT, amount INTEGER);
INSERT INTO txn VALUES
 (1, 'A', '2026-11-01',  -30),
 (2, 'A', '2026-11-02',  -90),
 (3, 'A', '2026-11-02',   50),
 (4, 'A', '2026-11-04',  -40),
 (5, 'A', '2026-11-05',  -10),
 (6, 'A', '2026-11-07',  100),
 (7, 'B', '2026-11-01',  200),
 (8, 'B', '2026-11-03',  -50),
 (9, 'B', '2026-11-06',  -25),
 (10,'C', '2026-11-02',  -60),
 (11,'C', '2026-11-03',   20),
 (12,'C', '2026-11-05',  -30),
 (13,'C', '2026-11-08',  -10),
 (14,'C', '2026-11-09',   90);

-- Q1
SELECT t.account, t.txn_date, t.amount,
       a.opening_balance
         + SUM(t.amount) OVER (PARTITION BY t.account ORDER BY t.txn_date, t.id) AS balance
FROM txn t
JOIN accounts a ON a.account = t.account
ORDER BY t.account, t.txn_date, t.id;

-- Q2
WITH bal AS (
  SELECT t.id, t.account, t.txn_date, a.opening_balance,
         a.opening_balance
           + SUM(t.amount) OVER (PARTITION BY t.account ORDER BY t.txn_date, t.id) AS balance
  FROM txn t
  JOIN accounts a ON a.account = t.account
)
SELECT account, MIN(txn_date) AS first_overdraft
FROM bal
WHERE balance < 0
GROUP BY account
ORDER BY account;

-- Q3
WITH bal AS (
  SELECT t.id, t.account, t.txn_date, a.opening_balance,
         a.opening_balance
           + SUM(t.amount) OVER (PARTITION BY t.account ORDER BY t.txn_date, t.id) AS balance
  FROM txn t
  JOIN accounts a ON a.account = t.account
),
peaks AS (
  SELECT account, balance,
         MAX(opening_balance,
             MAX(balance) OVER (PARTITION BY account ORDER BY txn_date, id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) AS peak_so_far
  FROM bal
)
SELECT a.account, COALESCE(MAX(p.peak_so_far - p.balance), 0) AS max_drawdown
FROM accounts a
LEFT JOIN peaks p ON p.account = a.account
GROUP BY a.account
ORDER BY a.account;

-- Q4
WITH bal AS (
  SELECT t.id, t.account, t.txn_date, a.opening_balance,
         a.opening_balance
           + SUM(t.amount) OVER (PARTITION BY t.account ORDER BY t.txn_date, t.id) AS balance
  FROM txn t
  JOIN accounts a ON a.account = t.account
),
flagged AS (
  SELECT account, balance < 0 AS neg,
         ROW_NUMBER() OVER (PARTITION BY account ORDER BY txn_date, id)
           - ROW_NUMBER() OVER (PARTITION BY account, balance < 0 ORDER BY txn_date, id) AS grp
  FROM bal
),
runs AS (
  SELECT account, COUNT(*) AS run_len
  FROM flagged
  WHERE neg
  GROUP BY account, grp
)
SELECT a.account, COALESCE(MAX(r.run_len), 0) AS longest_negative_streak
FROM accounts a
LEFT JOIN runs r ON r.account = a.account
GROUP BY a.account
ORDER BY a.account;
