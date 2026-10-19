# Day 28, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-27 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-25 see your own files; Day 26 static
actions; Day 27 CDS associations vs. compositions.)

## THE TASK

Pick ONE concept -- suggestions: CDS parameters / parameterised views,
RAP BO test doubles (`cl_botd_...`), the RAP generator, `%control` /
`%tky` structures, `internal` actions, `mapping for` in the behavior
definition, CDS extension views, or the `failed` / `reported` / `mapped`
response structures -- and explain it as if teaching a classmate who knows
classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

The `failed` / `reported` / `mapped` response structures in RAP.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you would raise an exception or fill a RETURN table with messages. In RAP, every handler method in a behavior implementation receives three response structures instead, which are collected and handed back to the framework (and in EML calls, to the caller).

`failed` says WHICH instances (identified by their keys, e.g. `%tky`) could not be processed, and why (`%fail-cause`, such as `not_found`, `unauthorized` or `locked`). It decides that the operation for those instances is aborted and, in the save sequence, that the transaction is not saved.

`reported` carries the MESSAGES shown to the user: each entry points at an instance (`%tky`), optionally at a field via `%element`, and holds a message object created with `new_message_with_text( )` or a message class. Reporting a message does not by itself fail anything: a warning or success message can be reported while processing continues. For a failure you usually append to both `failed` and `reported`.

`mapped` is used mostly in create operations: it returns the mapping between the temporary `%cid` that the caller supplied and the real (or final) key that was assigned, so the caller can refer to the new instance afterwards.

Think of it as: failed = what broke, reported = what to tell the user, mapped = which new key belongs to my %cid.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Reporting a message and failing an instance are separate: `reported` alone never aborts anything, so a validation must fill `failed` too. `mapped` is also filled in late numbering at save time (`mapped-late` handling), not just on early create. Always use `%tky` rather than bare keys so draft instances are addressed correctly.
