# Day 8, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-7, Task 9 -- pick a concept you have NOT
already written up. Day 3's pick was determinations vs. validations;
Day 4's was CDS view annotations for OData exposure; Day 5's was draft
handling; Day 6's was unmanaged vs. managed business objects; Day 7's
was optimistic concurrency / ETags; Day 2's pick is still TODO in
`day2-concept-notes.md`, so check that file too before choosing, to
avoid picking the same one twice.)

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project that you have NOT already written up -- for
example: early vs. late numbering for key generation, authorization
checks in a behavior definition (DCL -- Data Control Language),
OData V2 vs. V4 service exposure, the difference between an action and
a function in a behavior definition, virtual elements in a CDS view,
or the side-effects framework for triggering UI field refreshes -- and
explain it below in your own words, as if teaching a classmate who
knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Early vs. late numbering for key generation in RAP.

## MY EXPLANATION (write this BEFORE looking anything up)

Every RAP business object needs a unique key on each new instance. With early numbering the key is assigned as soon as the instance is created in the transactional buffer, in the `create`/`earlynumbering` handler method, before anything is saved, so the UI and later steps already know the real key. With late numbering the key is only assigned at the very end, in the save phase (the `adjust_numbers` method), just before the data is written to the database, and until then the instance only has a temporary key. Early numbering suits keys I can compute myself (a UUID or an external number); late numbering suits keys that must be gapless or that come from a number range and must not be wasted if the user cancels.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I first thought late numbering meant the key is assigned after the database insert, but it happens during the save sequence, before the actual INSERT, with the temporary key replaced by the final one. I was also fuzzy on the fact that with draft-enabled BOs, the draft table needs a key from the start, so managed UUID keys (early, `numbering:managed`) are the easy fit there, while number-range keys need extra care.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio project I'll use managed early numbering with a UUID key for the main entity, so drafts and the Fiori elements UI can refer to new instances immediately without any custom number-range code.
