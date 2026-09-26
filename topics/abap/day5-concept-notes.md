# Day 5, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-4, Task 9 -- pick a concept you have NOT
already written up. Day 3's pick was determinations vs. validations;
Day 4's pick was CDS view annotations for OData exposure; Day 2's pick
is still TODO in `day2-concept-notes.md`, so check that file too
before choosing, to avoid picking the same one twice.)

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project that you have NOT already written up -- for
example: authorization checks in a RAP behavior definition (DCL --
Data Control Language), early numbering vs. late numbering for key
generation, draft handling, unmanaged vs. managed business objects, or
exposing a service via OData V2 vs. V4 -- and explain it below in your
own words, as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

Draft handling in RAP (transactional buffer for unsaved changes on a
managed business object).

## MY EXPLANATION (write this BEFORE looking anything up)

Draft handling is how a RAP business object lets a user start editing something, save that half-finished work, and come back to it later without the change being visible to anyone else or committed to the database yet. Under the hood, every draft-enabled entity gets a shadow "draft table" alongside its normal active table; while a record is being edited it lives only in the draft table, tied to the editing user, and the active table is untouched. Only when the user explicitly activates/saves the draft (the RAP framework calls this "resume draft, then save") does the data get validated and copied into the active table in one transaction. In classic ABAP the closest analogy is a custom "working copy" Z-table you'd roll yourself with a status flag; RAP just gives you that pattern for free, wired into the Fiori Elements UI (the little "Draft saved" indicator) via standard annotations like @Semantics.draft and the draft-enabling behavior definition keyword `with draft`.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I initially assumed the draft table was just a copy of the active table's structure that RAP populates automatically with zero extra work, but it actually needs its own CDS entity and behavior projection (`with draft`) explicitly wired up, and the draft and active entities are genuinely separate persistences -- a query against the active entity's table will NOT see unsaved draft rows at all, which makes sense once you think about it (that's the whole point of drafts) but wasn't obvious to me up front. I also hadn't realized draft handling is what makes "early numbering" tricky: a key can get assigned to a draft row that never gets activated, so you can end up with permanently unused key values -- which is one reason late numbering is often preferred alongside drafts.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio project's order-entry app, draft handling is what will let a user start filling out a multi-line order, get pulled away, and resume it later from the Fiori Elements "drafts" list without a half-built order ever showing up in reports that read the active order table.
