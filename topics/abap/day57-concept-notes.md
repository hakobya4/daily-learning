# Day 57, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: ABAP SQL common table expressions and modern SELECT features (`WITH +cte AS ( ... )`, `SELECT ... FROM @itab AS t` to join an internal table, window expressions `OVER( PARTITION BY ... )`, and how pushing logic into the database this way differs from `SELECT` + `LOOP` in classic reports), table buffering (single-record / generic / full buffering in SE11, which statements bypass the buffer -- `BYPASSING BUFFER`, aggregates, joins -- and why buffering a frequently-updated table is a bad idea), or the SAP LUW and update tasks (`CALL FUNCTION ... IN UPDATE TASK`, `PERFORM ... ON COMMIT`, `COMMIT WORK` vs. `COMMIT WORK AND WAIT`, `SET UPDATE TASK LOCAL`, and why a BAPI needs `BAPI_TRANSACTION_COMMIT`) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP or modern ABAP syntax.

## CONCEPT CHOSEN

The SAP LUW and update tasks: `CALL FUNCTION ... IN UPDATE TASK`, `PERFORM ... ON COMMIT`,
`COMMIT WORK` vs. `COMMIT WORK AND WAIT`, `SET UPDATE TASK LOCAL`, and why a BAPI needs
`BAPI_TRANSACTION_COMMIT`.

## MY EXPLANATION (write this BEFORE looking anything up)

**Two different "units of work".** The database has its own transaction, the *database
LUW*: everything between two database commits. In an SAP system a database commit
happens far more often than you think -- the work process does an implicit DB commit at
the end of every dialog step (every screen change, every `MESSAGE` of type I/S/W that
waits for the user, every RFC call, `WAIT UP TO`), because the work process is handed to
another user afterwards. A business transaction such as "create a sales order" spans
several screens, so it cannot be one database LUW. The *SAP LUW* is the logical unit
that SAP builds on top: all changes that must be written together or not at all, no
matter how many dialog steps it took to collect them. It ends with `COMMIT WORK`
(write everything) or `ROLLBACK WORK` (throw everything away).

**How the SAP LUW achieves "all or nothing": bundling.** Instead of executing
`INSERT`/`UPDATE` immediately (which would be committed by the next implicit DB commit),
you *register* the change and execute it later, in one go:

* `CALL FUNCTION 'Z_SAVE_ORDER' IN UPDATE TASK EXPORTING ...` -- the function module must
  be flagged as an *update module* in SE37. The call does not run now; the module name
  and a copy of its parameters are written to the update tables (VBHDR / VBMOD /
  VBDATA) under a common *update key*.
* `PERFORM save_log ON COMMIT` -- a subroutine registered in the current program; it runs
  in the same work process right at `COMMIT WORK` (only once, even if registered
  several times; `ON ROLLBACK` exists as well).

**What `COMMIT WORK` does.** It first runs all `PERFORM ... ON COMMIT` routines, raises
the event that closes the SAP LUW, and then hands the update key to the *update work
process* (type UPD/V1). That process executes all registered update modules in ONE
database LUW: if any of them fails (a `MESSAGE TYPE 'A'` or a runtime error), the whole
update is rolled back, the user gets an express mail / the entry shows up in SM13 as
erroneous, and nothing is partially written. Plain `COMMIT WORK` is **asynchronous**:
your program continues immediately while the update runs in the background. That is
why a classic bug is "I `COMMIT WORK` and then `SELECT` my new document and it is not
there yet".

* `COMMIT WORK AND WAIT` makes it **synchronous**: the program waits until the V1 update
  has finished, and you can check `sy-subrc` (0 = update succeeded). Use it when the next
  step needs the data (read it back, call another BAPI that depends on it).
* `SET UPDATE TASK LOCAL` (must be set before the first update call in the LUW, and is
  reset by every commit) makes the update modules run *locally* in the current dialog
  work process instead of the update work process -- synchronous as well, no SM13
  entry, no extra process, and nothing is written to VBDATA, which is handy in batch
  jobs and mass processing.
* V1 vs. V2: V1 modules are the time-critical ones (the document itself) and run first
  in one DB LUW; V2 modules ("update with delayed start", e.g. statistics) run afterwards
  in a separate LUW, so a V2 failure does not undo the V1 document.

**Locks belong to the same story.** SAP enqueue locks (`ENQUEUE_EZ...`) taken with
`_scope = 2` (the default) are passed to the update task at `COMMIT WORK` and released
only after the update has finished -- so nobody can change the object between "the user
pressed save" and "the update actually wrote it".

**Why BAPIs need `BAPI_TRANSACTION_COMMIT`.** BAPIs follow the same pattern: e.g.
`BAPI_SALESORDER_CREATEFROMDAT2` validates the data and *registers* its update modules,
but by design it never commits itself, so the caller can bundle several BAPIs into one
SAP LUW and decide at the end. If you only call the BAPI, check `RETURN` and stop, the
order is never saved -- the registered updates are discarded when the program/RFC
session ends. You must call `BAPI_TRANSACTION_COMMIT` (usually with `WAIT = 'X'`, which
is `COMMIT WORK AND WAIT`) when `RETURN` has no `E`/`A` messages, or
`BAPI_TRANSACTION_ROLLBACK` otherwise. Over RFC (e.g. from an external program) you
can't write `COMMIT WORK` yourself, so these two BAPIs are the remote-callable way to end
the LUW -- and they must be called in the **same RFC session** as the BAPI, otherwise
they commit an empty LUW. Inside ABAP you could technically write `COMMIT WORK`, but the
BAPI wrappers also reset BAPI-internal buffers, so the convention is to always use them.

**Rules of thumb I take from this:**
1. Never `COMMIT WORK` inside an update module, a BAdI or a user exit -- you would break
   the caller's LUW (in an update module it is even a runtime error).
2. Don't do direct `INSERT/UPDATE` on DB tables in the middle of a dialog transaction --
   they get committed at the next dialog step and can't be rolled back with the rest.
3. Use `COMMIT WORK AND WAIT` (or `BAPI_TRANSACTION_COMMIT` with `WAIT = 'X'`) whenever
   the next statement depends on the written data.
4. In RAP this is all hidden: `COMMIT ENTITIES` triggers the save sequence, and the
   framework forbids explicit `COMMIT WORK` in behavior implementations for exactly the
   same "one LUW" reason.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

* I used to think the implicit database commit only happens on `COMMIT WORK`. In fact
  every dialog step / RFC / `WAIT` ends the database LUW -- which is the whole reason the
  SAP LUW and the update task exist.
* `PERFORM ... ON COMMIT` runs in the *dialog* work process before the update task is
  triggered, not in the update work process; and if the same form is registered several
  times it still runs only once (parameters come from the global data at commit time,
  since `ON COMMIT` forms cannot take `USING` parameters).
* `COMMIT WORK AND WAIT` only waits for the V1 update; V2 updates still run later.
* `SET UPDATE TASK LOCAL` is reset by each `COMMIT WORK`/`ROLLBACK WORK`, so in a loop
  that commits per document it has to be set again for every LUW.
* `BAPI_TRANSACTION_COMMIT` without `WAIT = 'X'` is an asynchronous commit -- reading
  the created document right afterwards can fail for exactly the same reason as plain
  `COMMIT WORK`.
