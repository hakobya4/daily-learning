# Day 21, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-20 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events.)

## THE TASK

Pick ONE concept -- suggestions: the RAP BO test double framework (EML
test doubles), CDS associations vs. compositions, the additional save /
unmanaged save in a managed BO, CDS table functions, or the RAP
generator / service binding types (OData V2 vs. V4, UI vs. Web API) --
and explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

Additional save and unmanaged save in a managed RAP business object.

## MY EXPLANATION (write this BEFORE looking anything up)

In a managed RAP BO the framework does the persistence for you: during the save sequence it writes the changes of the BO's entities to the database tables you mapped. Sometimes that is not enough. You may need to write to an extra table (a log, a change-document, an index), call a legacy function module or an API, or send out data in the same LUW. RAP lets you do that without giving up "managed".

With `with additional save` in the behavior definition, the managed runtime still performs its own database writes, and then additionally calls the `save_modified` method of a saver class (`CLASS lsc_... DEFINITION INHERITING FROM cl_abap_behavior_saver`). In `save_modified` you receive the `create`, `update` and `delete` tables, containing the changed instances (and, via `%control`, which fields changed), and you do whatever extra persistence you need. If you declare `with unmanaged save`, the framework skips its own writes for that entity and you are fully responsible for persisting, which is useful when the data goes to a legacy API rather than to the mapped table.

The classic-ABAP analogy: managed = the framework generates the "update task" for you; additional save = a hook at the end of PERFORM ON COMMIT where you add your own updates. It runs only in the save phase of the interaction phase / save sequence (after `finalize` and `check_before_save` succeeded), so you must not do anything that can fail or raise messages, no COMMIT WORK, and no DB writes in the interaction phase.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Things to keep straight: additional save adds to the managed save, unmanaged save replaces it; saver methods must not commit or raise business errors (validations belong in `check_before_save`/validations earlier); and the saver is called once per BO per save with all changed instances, so work in bulk. I initially thought unmanaged save meant the whole BO becomes unmanaged, but it only replaces the persistence step for that entity; determinations, validations and actions still work as usual.
