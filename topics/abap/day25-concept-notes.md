# Day 25, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-24 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 23 factory actions; Day 24 see your own file;
Day 21-22 see your own files.)

## THE TASK

Pick ONE concept -- suggestions: `with additional save`, static actions,
CDS parameters / parameterised views, RAP BO test doubles, the RAP
generator, `cleanup` / `cleanup finalize` in the save sequence,
`%control` / `%tky` structures, or `internal` actions -- and explain it
as if teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

`with additional save` (and `cleanup`) in the RAP save sequence

## MY EXPLANATION (write this BEFORE looking anything up)

In a managed RAP business object the framework does the database writes
for you at the end of the transaction: it collects all the changes made
during the interaction phase and persists them in the save phase. Usually
that is exactly what you want. But sometimes you also need something extra
at save time: writing a change-document, calling a legacy function module
that does its own updates, or filling a second table the BO does not own.

`with additional save` is added to the behavior definition (for the whole
BO or one entity). It tells the framework: still do the standard managed
save, and in addition call my own `save_modified` method in the behavior
pool. In `save_modified` you get the `create`, `update` and `delete`
structures with the changed instances, and you can do the extra persistence
there. The rule is that it only runs in the save phase, after the checks
(validations) have passed, so you must not raise business errors there and
you must not do a COMMIT yourself, because the framework owns the commit.

`cleanup` is the opposite end: if the transaction is rolled back, the
`cleanup` method resets any transactional buffers you keep in your class so
the next request starts clean. Think of classic ABAP: `with additional save`
is like a `PERFORM ... ON COMMIT`, and `cleanup` is like
`PERFORM ... ON ROLLBACK`.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- `save_modified` belongs to the saver class (`lsc_...` inheriting from
  `cl_abap_behavior_saver`), not the handler class.
- `with unmanaged save` is different: it replaces the managed save
  completely, while `with additional save` keeps it and adds to it.
- `cleanup` is called on rollback paths and `cleanup_finalize` after the
  save phase, to clear buffers either way.
