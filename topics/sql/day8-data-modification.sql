-- Day 8, Task 2 -- SQL: data modification (UPDATE, DELETE, INSERT...SELECT).
--
-- Self-contained: schema + data + statements all in this one file.
-- Load it with: sqlite3 practice_day8b.db < day8-data-modification.sql
--
-- Nothing below is pre-solved. Write each statement yourself, IN
-- ORDER -- each one's expected result assumes the previous statements
-- already ran, since UPDATE/DELETE/INSERT actually change the data
-- (unlike every SELECT-only exercise so far).

DROP TABLE IF EXISTS transactions_sql;
DROP TABLE IF EXISTS archived_accounts_sql;
DROP TABLE IF EXISTS accounts_sql;

CREATE TABLE accounts_sql (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    balance REAL NOT NULL
);

CREATE TABLE transactions_sql (
    id         INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts_sql(id),
    amount     REAL NOT NULL
);

-- same shape as accounts_sql, on purpose -- Q3 archives into it.
CREATE TABLE archived_accounts_sql (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    balance REAL NOT NULL
);

INSERT INTO accounts_sql (id, name, balance) VALUES
    (1, 'Amara', 100),
    (2, 'Ben',   200),
    (3, 'Chen',  50),
    (4, 'Dana',  300),
    (5, 'Eli',   20);

INSERT INTO transactions_sql (id, account_id, amount) VALUES
    (1, 1, 50),
    (2, 2, 30),
    (3, 4, 100);
-- note: accounts 3 (Chen) and 5 (Eli) have NO rows in transactions_sql
-- at all -- deliberate, for Q2's "never transacted" delete.

-- Q1: The average balance across ALL 5 accounts right now is 134
-- ((100+200+50+300+20)/5). UPDATE accounts_sql to give every account
-- whose balance is BELOW that average a 10% raise (balance = balance
-- * 1.1), using a scalar subquery for the average in the WHERE
-- clause -- don't hardcode 134.
-- Expected after this UPDATE: Amara 110, Ben 200 (unchanged, was
-- already >= average), Chen 55, Dana 300 (unchanged), Eli 22.
-- TODO: write this statement.


-- Q2: DELETE every account that has NEVER appeared in
-- transactions_sql at all (an anti-join style condition -- account id
-- NOT IN (SELECT account_id FROM transactions_sql), or a NOT EXISTS
-- correlated subquery -- either is fine).
-- Expected after this DELETE: only Amara, Ben, and Dana remain (Chen
-- and Eli, having never transacted, are gone).
-- TODO: write this statement.


-- Q3: INSERT INTO archived_accounts_sql ... SELECT ... every account
-- STILL remaining in accounts_sql whose balance is above 250 (copy
-- the row over, don't just reference it -- archived_accounts_sql is a
-- separate table).
-- Expected: archived_accounts_sql ends up with exactly one row --
-- Dana, 300 (Amara's 110 and Ben's 200 are both below the 250 cutoff).
-- TODO: write this statement.
