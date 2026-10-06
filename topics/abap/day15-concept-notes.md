# Day 15, Task 10 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-14 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags/optimistic concurrency; Day 8 early vs. late
numbering; Day 9 actions vs. functions; Day 10 authorization control;
Day 11 side effects; Day 12 feature control; Day 13 the save sequence;
Day 14 value helps.)

## THE TASK

Pick ONE concept -- suggestions: virtual elements in CDS, the RAP BO test
double framework (`cl_botd_*`), CDS associations vs. compositions,
`%control` / `%tky` / `%key` in EML, projection views and behavior
projections, or `READ ENTITIES` / `MODIFY ENTITIES` / `COMMIT ENTITIES`
-- and explain it as if teaching a classmate who knows classic ABAP but
has never touched RAP.

## CONCEPT CHOSEN

EML: READ ENTITIES / MODIFY ENTITIES / COMMIT ENTITIES (Entity Manipulation Language), including %tky / %key / %control.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP I would read and update business data with SELECT and
UPDATE/INSERT statements directly on the tables, which skips any business
logic. EML is the RAP way to talk to a business object through its behavior
instead of the tables. READ ENTITIES reads instances of an entity, MODIFY
ENTITIES creates, updates, deletes or triggers actions on them, and nothing is
written to the database until COMMIT ENTITIES runs the save sequence. Because
all changes go through the behavior, determinations and validations run just as
they would from a Fiori app. Keys are passed as %tky (the transactional key,
which also covers draft), and %control flags tell RAP which fields I actually
set, so unset fields are not overwritten with initial values.

## WHAT I GOT RIGHT / WRONG (after checking the docs)

Right: EML goes through the behavior, and COMMIT ENTITIES is what triggers the
save. Fuzzy: %tky is not the same as %key - %key holds only the semantic key
fields, while %tky additionally includes %is_draft, so use %tky for draft-enabled
BOs. Also, READ/MODIFY return results into response tables (FAILED, REPORTED,
MAPPED) that I must check, and in a RAP handler method I don't call COMMIT ENTITIES
myself, because the framework owns the save sequence.

## ONE SMALL EXAMPLE

```abap
MODIFY ENTITIES OF zi_travel
  ENTITY Travel
    UPDATE FIELDS ( Description )
    WITH VALUE #( ( %tky = key-%tky Description = 'Updated via EML' ) )
  FAILED   DATA(failed)
  REPORTED DATA(reported).

IF failed IS INITIAL.
  COMMIT ENTITIES RESPONSE OF zi_travel
    FAILED   DATA(commit_failed)
    REPORTED DATA(commit_reported).
ENDIF.
```
Here UPDATE FIELDS makes RAP set only the Description flag in %control, so other fields stay untouched.
