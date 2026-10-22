# Day 31, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-30 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-25 see your own files; Day 26 static
actions; Day 27 CDS associations vs. compositions; Day 28-30 see your
files.)

## THE TASK

Pick ONE concept -- suggestions: CDS parameters / parameterised views,
RAP BO test doubles (`cl_botd_...`), the RAP generator, `%control` /
`%tky` structures, `internal` actions, CDS extension views, ABAP Unit with
the SQL test double framework, `FOR ALL ENTRIES` vs. CDS joins, or
RAP `with additional save` -- and explain it as if teaching a classmate
who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

RAP `with additional save` (additional save in the save sequence).

## MY EXPLANATION (write this BEFORE looking anything up)

In a managed RAP business object the framework writes the changed data to the database tables for you during the save phase. Sometimes that is not enough: you also want to write a change-log row, call a legacy function module / update task, or send something to another system, but only once the transaction is really going to be committed. That is what `with additional save` is for. You add it to the behavior definition (`with additional save` on the entity, or `save_modified` in the unmanaged variant) and implement the save method `save_modified` in the saver class (`lsc_<bo>` inheriting from `cl_abap_behavior_saver`). The framework still does its own managed persistence, and then it calls your `save_modified` with the `create`, `update` and `delete` parameters containing exactly what changed in this LUW.

The comparison to classic ABAP: it is like putting `CALL FUNCTION ... IN UPDATE TASK` or a `PERFORM ... ON COMMIT` hook that only runs when the final COMMIT WORK happens. Because it runs in the save phase (after the interaction phase and `finalize`/`check_before_save` succeeded), no COMMIT or ROLLBACK is allowed there and no EML modifications either; you only do database/side-effect work. If the interaction phase failed, the saver is never called, so no half-written log entries exist. With `unmanaged save` you replace the framework's persistence entirely; with `with additional save` you only add to it.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- The method is called `save_modified` and it receives the changes with the `%control` flags, so for updates you must check which fields were really changed rather than assume the whole row is new.
- Do not mix it up with `additional save` inside actions: it belongs to the save sequence (`adjust_numbers`, `save`, `cleanup`), not to the interaction phase, so reading with EML there is not allowed.
- With draft, additional save runs only when the draft is activated (Prepare/Activate), not on every draft save.
- Use `unmanaged save` when you must replace the persistence; use `with additional save` when you only want extra side effects such as logging or numbering-dependent writes.
