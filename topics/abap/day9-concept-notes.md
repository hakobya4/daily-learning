# Day 9, Task 9b -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-8 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags/optimistic concurrency; Day 8 early vs. late
numbering. Day 2's is still TODO in `day2-concept-notes.md`.)

## THE TASK

Pick ONE concept -- suggestions: actions vs. functions in a behavior
definition, authorization control with DCL (`define role`), virtual
elements in CDS, side effects for UI refresh, or value helps
(`@Consumption.valueHelpDefinition`) -- and explain it as if teaching a
classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Actions vs. functions in a RAP behavior definition.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP, if I wanted a button like "Approve order" I would write
a function module or a method and call it from a screen. In RAP the
same idea is declared in the behavior definition and implemented in the
behavior pool. An **action** is a custom operation on a business object
instance that can CHANGE data: e.g. `action approve result [1] $self;`
sets a status field and the framework saves it in the same transaction
(and handles draft, locking, and authorization for it). A **function**
is a custom operation that only READS: it returns a value or entity
data and must not modify the state of the business object, e.g.
`function getDiscount result [1] ...`. Both can be instance-bound (work
on selected rows) or static (no instance, like a factory), and both
are exposed in the service so Fiori can show a button that calls them.
The rule of thumb: side effects -> action; pure query -> function.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

- Actions can have an input parameter (`parameter ZD_MyStructure`) that
  opens a small dialog in Fiori; I had forgotten that part.
- The result of an action is often `$self`, which makes the UI refresh
  the changed instance without an extra read.
- A function is not allowed to change the BO, but it is still checked
  for authorization; being read-only does not mean unprotected.
- Factory actions (`factory action copy [1]`) create new instances and
  are a third flavour I should study separately.
- I should double-check exact keyword syntax in the RAP documentation
  before relying on my examples above.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio RAP app, status changes (e.g. confirming or cancelling a
booking/order) belong in instance actions such as `confirm` and
`cancel`, with feature control (`features : instance`) to disable them
in the wrong status. Read-only helpers, such as calculating a total or
a suggested value, would be functions instead. This keeps the business
logic in the behavior pool and out of the UI.
