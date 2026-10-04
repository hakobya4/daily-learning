# Day 13, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-12 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags/optimistic concurrency; Day 8 early vs. late
numbering; Day 9 actions vs. functions; Day 10 authorization control;
Day 11 side effects; Day 12 feature control.)

## THE TASK

Pick ONE concept -- suggestions: virtual elements in CDS, value helps
(`@Consumption.valueHelpDefinition`), the RAP save sequence
(interaction phase vs. save phase, `additional save`, `with unmanaged
save`), the RAP BO test double framework, CDS associations vs.
compositions, or `%control` / `%tky` / `%key` in EML -- and explain it
as if teaching a classmate who knows classic ABAP but has never
touched RAP.

## CONCEPT CHOSEN

The RAP save sequence: interaction phase vs. save phase.

## MY EXPLANATION (write this BEFORE looking anything up)

A RAP transaction has two phases. In the interaction phase the consumer
(Fiori app or EML code) calls operations such as create, update, delete
and actions; the framework runs determinations and validations on a
transactional buffer in memory, and nothing is written to the database
yet. The consumer can read back the buffered state in the same
transaction. When the consumer commits (`COMMIT ENTITIES`, or the
framework does it at the end of an OData request), the save phase starts:
the framework runs the final checks (`finalize`, `check_before_save`),
then `adjust_numbers` for late numbering, and then `save`, which writes
the buffer to the database. In a managed BO the framework does the save
for me. In an unmanaged BO I implement `save` myself, and with `with
unmanaged save` or `additional save` I can add my own writes, for example
calling a function module or writing a change document, on top of the
managed one. If any validation fails the whole transaction is rolled back
instead of saved. It is like classic ABAP where the PAI collects changes
in internal tables and `PERFORM ... ON COMMIT` or update function modules
write them only at the commit.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I was fuzzy on the exact order of the save-phase methods: it is `finalize`,
then `check_before_save`, then `adjust_numbers` (late numbering only), then
`save`, then `cleanup`. Also, database writes must happen ONLY in the save
phase, never in the interaction phase; the interaction-phase methods must not
call `COMMIT WORK` or do direct DB modifications.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my RAP portfolio project the validations and determinations run during
the interaction phase, so users see errors early. If I add audit logging
I would put it in `additional save` so it only happens when the
transaction really commits.
