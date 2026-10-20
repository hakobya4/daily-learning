# Day 30, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-29 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-25 see your own files; Day 26 static
actions; Day 27 CDS associations vs. compositions; Day 28-29 see your
files.)

## THE TASK

Pick ONE concept -- suggestions: CDS parameters / parameterised views,
RAP BO test doubles (`cl_botd_...`), the RAP generator, `%control` /
`%tky` structures, `internal` actions, `mapping for` in the behavior
definition, CDS extension views, `FOR ALL ENTRIES` vs. CDS joins, or
numbering with `managed ... early numbering` -- and explain it as if
teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

`mapping for` in the behavior definition (field mapping between the CDS entity and the database table).

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you read and write a database table directly, so the field names in your code are the column names. In RAP the business object is built on a CDS view entity, and CDS element names are usually camel-cased (`TravelId`, `BeginDate`) while the table columns are old style (`travel_id`, `begin_date`). The managed runtime has to write the changed CDS fields into the table on save, and it cannot guess how the names line up. The `mapping for <table> corresponding { ... }` block in the behavior definition tells it: each line is `CdsElement = table_column`. With `corresponding`, fields whose names already match are mapped automatically and you list only the exceptions. Think of it as the translation table between the business view of the data and the persistence layer. It is needed for managed BOs with a persistent table; for unmanaged ones you write the save logic yourself, and projection layers do not map because they reuse the base entity.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

`corresponding` only maps fields that match by name, so every renamed field still needs an explicit line, and the mapping is per table (the root and each child entity have their own `mapping for`). Unmapped, non-virtual CDS fields cause a syntax warning or error, and the `%control` structure for an element follows the same mapping to know which columns to update. Draft tables are generated from the draft definition, so they need no separate mapping.
