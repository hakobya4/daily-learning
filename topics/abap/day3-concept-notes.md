# Day 3, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Day 2, Task 9 -- pick a DIFFERENT concept than last
time so you build up more than one written explanation over time.)

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project that you have NOT already written up -- for
example: CDS view annotations, determinations vs. validations, draft
handling, unmanaged vs. managed BOs, or exposing an OData service --
and explain it below in your own words, as if teaching a classmate who
knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Determinations vs. validations in a RAP behavior definition (different
from Day 2's pick, which is still open).

## MY EXPLANATION (write this BEFORE looking anything up)

Both determinations and validations are hooks that fire during a RAP
transaction, but they answer two different questions. A determination
CHANGES data -- it's for "when X happens, automatically set Y." For
example, when a sales order line is created, a determination can
default its currency from the header, or stamp a `created_by` field,
without the user having to type it. A validation, on the other hand,
never changes data -- it only CHECKS it and raises a `%msg` failed
state if something is wrong, like refusing to save an order line whose
quantity is negative. The other big difference is trigger timing: a
determination runs `on save` or `on modify` (i.e., as soon as the
triggering field changes, even before save), while a validation
usually runs `on save`, because you generally want to check the final,
fully-determined state of the data rather than a half-edited draft.
In classic ABAP terms, a determination is closest to a BAdI that
enriches data before it's persisted; a validation is closest to the
authority/consistency checks you'd hand-write in a `CHECK` routine
before a `COMMIT WORK`.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I initially assumed determinations could also block a save (like a
validation) if the derived value turned out to be invalid -- that's
not right; a determination only sets fields, it doesn't fail the
operation. If a derived value needs to be checked, the pattern is to
have the determination set it and a separate validation check it
afterward. I was also fuzzy on `on modify` vs `on save` triggers for
determinations: `on modify` fires as soon as the relevant field
changes in the current transaction (so the UI can reflect it live,
useful for something like a computed total), while `on save` only
fires right before persistence -- I'd been treating those as
interchangeable, but they change what the user sees mid-edit.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

I'm using a determination to default a `status` field to `'NEW'` when
a record is created, and a validation to reject any record where a
required reference field is left blank before it's allowed to save --
keeping those as two separate, single-purpose hooks instead of one
tangled "do everything" method is the main lesson I want the project
to demonstrate.
