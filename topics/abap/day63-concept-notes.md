# Day 63, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: SAP lock objects and the enqueue server (defining a lock object in SE11, the generated `ENQUEUE_E...` / `DEQUEUE_E...` function modules, lock modes `E` / `S` / `X` / `O`, the `_SCOPE` parameter and how locks interact with the SAP LUW, inspecting locks in SM12, and why a lock is a logical agreement between programs rather than a database lock), ABAP Unit test isolation (test classes with `FOR TESTING`, `RISK LEVEL` / `DURATION`, `setup` / `teardown`, `cl_abap_unit_assert`, and how to replace dependencies with test doubles: constructor injection + interfaces, `cl_abap_testdouble`, test seams `TEST-SEAM` / `TEST-INJECTION`, and `cl_osql_test_environment` for faking database tables), or the SALV object model for ALV output (`cl_salv_table=>factory`, columns via `get_columns( )` / `cl_salv_column_table`, sorts, aggregations, functions/toolbar, and event handling for `double_click` / `added_function`, versus the old `REUSE_ALV_GRID_DISPLAY` and `cl_gui_alv_grid`) -- and explain it as if teaching a classmate who knows classic ABAP report programs, internal tables and `SELECT`, but has never used this feature.

## CONCEPT CHOSEN

SAP lock objects and the enqueue server: defining a lock object in SE11, the generated
`ENQUEUE_E...` / `DEQUEUE_E...` function modules, lock modes, `_SCOPE`, and SM12.

## MY EXPLANATION (write this BEFORE looking anything up)

**The problem.** Two users open the same sales order in change mode. Both read it, both
edit, both save -- the second save silently overwrites the first ("lost update"). Database
row locks don't help here: in SAP a single business transaction spans several dialog
steps, and every dialog step ends with an implicit DB commit, which releases all
database locks. So SAP needs locks that live *longer* than one database transaction and
that every program agrees to respect. That is what the enqueue service provides.

**How it works.** There is one central lock table per system, held in main memory by the
enqueue server (classically on the central instance, today the Standalone Enqueue Server
in ASCS). A lock entry is basically "table + key values + lock mode + owner". Programs
never touch that table directly; they call generated function modules:

- In SE11 you create a **lock object** whose name must start with `E` (e.g. `EZ_ORDER`).
  You list the primary table (and optionally secondary tables linked by foreign keys),
  choose a default lock mode, and pick the **lock parameters** -- usually the key fields.
- Activating it generates two function modules: `ENQUEUE_EZ_ORDER` (set the lock) and
  `DEQUEUE_EZ_ORDER` (release it). Their importing parameters are the lock parameters
  plus `MODE_<table>`, `X_<field>`, `_SCOPE`, `_WAIT` and `_COLLECT`.
- Leaving a key parameter empty means "all values" (a generic lock), unless you set the
  matching `X_<field> = 'X'`, which means "lock exactly the initial value".

**Lock modes.**

- `E` (exclusive, cumulative): write lock. Other users can't get any lock on the same
  key, but the *same* transaction can request it again (it is counted up).
- `X` (exclusive, non-cumulative): like `E` but even the same owner can't request it
  twice -- protects against re-entering your own code path.
- `S` (shared): read lock. Many `S` locks can coexist; they block `E`/`X` requests from
  others. Use it when you need the data not to change while you read/compute.
- `O` (optimistic): coexists with `S` and other `O` locks; it is promoted to `E` at
  save time (via mode `R`), and promotion fails if someone else changed in between. It
  is used by frameworks rather than by hand.

If the key is already locked by someone else, the enqueue FM raises the exception
`FOREIGN_LOCK`, and `sy-msgv1` holds the user that owns it -- so you can show
"Order 4711 is currently being processed by user MEIER". `SYSTEM_FAILURE` means the
enqueue server couldn't be reached.

**`_SCOPE` and the SAP LUW.** Locks are tied to an owner. `_SCOPE` decides who owns it:

- `1` -- the dialog program owns it; released when the program ends or you call DEQUEUE.
  The update task does NOT inherit it.
- `2` (default) -- the lock is handed over to the update task at `COMMIT WORK`; it is
  released automatically when the update task finishes (or at `ROLLBACK WORK`). This is
  the normal case: lock in dialog, write in `IN UPDATE TASK` FMs, the lock stays until
  the data is really in the database.
- `3` -- both owners hold it; it is only gone after both have released it.

**It is only a convention.** The enqueue lock does not physically stop an `UPDATE` on
the table. A program that skips the ENQUEUE call can still overwrite the row. Locks
work because every program that changes `ZORDERS` follows the same rule: "enqueue first,
re-read the data after getting the lock, then change it". That's also why you re-read
*after* the lock succeeds -- the row could have changed between your first SELECT and the
lock.

**Tools.** SM12 lists current lock entries (user, table, argument, mode) and lets an
admin delete orphaned ones (dangerous -- only when the owner is really gone). SM12 also
has test functions to provoke lock errors. ST05 can trace enqueue calls.

**When to use / not use.** Use it for every classic dialog or background program that
changes business data which others might change concurrently. Keep locks short and
granular (one document, not the whole table). In RAP/Fiori stateless apps you don't call
ENQUEUE yourself -- the framework uses `lock master` (which internally calls the enqueue
service) plus ETags for optimistic checks, which I covered on days 17/35/44.

## A SMALL EXAMPLE

```abap
* Lock object EZ_ORDER in SE11: primary table ZORDERS, lock parameter ORDER_ID,
* default mode E. Activation generated ENQUEUE_EZ_ORDER / DEQUEUE_EZ_ORDER.

PARAMETERS p_order TYPE zorders-order_id OBLIGATORY.
PARAMETERS p_stat  TYPE zorders-status   DEFAULT 'S'.

START-OF-SELECTION.
  CALL FUNCTION 'ENQUEUE_EZ_ORDER'
    EXPORTING
      mode_zorders   = 'E'
      order_id       = p_order
      _scope         = '2'          " hand the lock to the update task at COMMIT
      _wait          = abap_false
    EXCEPTIONS
      foreign_lock   = 1
      system_failure = 2
      OTHERS         = 3.
  CASE sy-subrc.
    WHEN 1.
      MESSAGE |Order { p_order } is locked by user { sy-msgv1 }| TYPE 'E'.
    WHEN 2 OR 3.
      MESSAGE 'Lock service not available' TYPE 'E'.
  ENDCASE.

  " re-read AFTER the lock: the row may have changed since the screen was shown
  SELECT SINGLE * FROM zorders WHERE order_id = @p_order INTO @DATA(ls_order).
  IF sy-subrc <> 0.
    CALL FUNCTION 'DEQUEUE_EZ_ORDER' EXPORTING order_id = p_order.
    MESSAGE |Order { p_order } not found| TYPE 'E'.
  ENDIF.

  ls_order-status = p_stat.
  CALL FUNCTION 'Z_ORDER_UPDATE' IN UPDATE TASK
    EXPORTING is_order = ls_order.

  COMMIT WORK.   " lock (scope 2) now belongs to the update task and is released
                 " automatically once Z_ORDER_UPDATE has written the row
  MESSAGE |Order { p_order } saved| TYPE 'S'.
```

## WHAT I GOT WRONG / CHECKED AFTERWARDS

- I first thought `S` locks block other `S` locks -- they don't; shared locks are
  compatible with each other and only conflict with `E`/`X` from other owners.
- An empty lock parameter is a *generic* lock on all values, not "lock the empty key";
  that needs `X_<field> = 'X'`. Easy way to accidentally lock a whole table.
- The default `_SCOPE` is `2`, not `1`. With scope 1 and an update-task write, the lock
  is released when the dialog program ends, possibly before the update task has run.
- `DEQUEUE_ALL` releases every lock of the current owner -- handy in error paths, but it
  also drops locks set by other parts of the same transaction.

## ONE-LINE TAKEAWAY

An SAP lock is a cross-dialog-step logical agreement kept by the enqueue server: enqueue
the key, re-read, change via the update task, and let `_SCOPE = 2` release it after the
data is really committed.
