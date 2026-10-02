# Day 11, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-10 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags/optimistic concurrency; Day 8 early vs. late
numbering; Day 9 actions vs. functions; Day 10 authorization control.)

## THE TASK

Pick ONE concept -- suggestions: virtual elements in CDS (calculated in
ABAP at read time), side effects (`side effects { field X affects field
Y; }`) for UI refresh, value helps (`@Consumption.valueHelpDefinition`),
the RAP save sequence (interaction phase vs. save phase, `additional
save`, `with unmanaged save`), or the RAP BO test double framework for
unit-testing behavior -- and explain it as if teaching a classmate who
knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Side effects (`side effects { field X affects field Y; }`) for UI refresh in RAP.

## MY EXPLANATION (write this BEFORE looking anything up)

In a Fiori elements app on RAP, when a user edits a field the UI does not
automatically know that other fields or the whole instance may have changed
on the backend. Say the user changes Quantity and a determination
recalculates TotalPrice: without help, TotalPrice on screen stays stale
until the page is reloaded. A side effect declaration in the behavior
definition tells the framework: "when field X changes, re-read field Y
(or these other fields, or the whole entity)". For example
`side effects { field Quantity affects field TotalPrice; }`. You can also
say an action affects fields, or that a field affects messages, or entire
entities. After the field change the UI sends a follow-up read (a
side-effects request) only for the affected targets, so the screen
refreshes without a full reload, and it is cheaper than reloading everything.
In classic ABAP dynpro I would have recalculated in PAI/PBO; here the
server-side logic stays in determinations, and the side effect only
declares which parts of the UI must be re-fetched.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

- Side effects do not compute anything; determinations do the calculation, and side effects just trigger a re-read in the UI. I should not mix the two up.
- Targets can be fields, entities, or `$self` (the whole instance); with draft, determinations on modify run when the draft is updated, so the side effect fetches the updated values.
- There are also `determine action` and `determine on save` pieces for validation timing that I should read more about.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio RAP app, any calculated field (totals, status derived from other fields) updated by a determination would need a side effect so the Fiori UI shows the new value immediately after an edit, instead of only after a refresh.
