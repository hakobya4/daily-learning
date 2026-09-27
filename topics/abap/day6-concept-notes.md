# Day 6, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-5, Task 9 -- pick a concept you have NOT
already written up. Day 3's pick was determinations vs. validations;
Day 4's was CDS view annotations for OData exposure; Day 5's was draft
handling; Day 2's pick is still TODO in `day2-concept-notes.md`, so
check that file too before choosing, to avoid picking the same one
twice.)

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project that you have NOT already written up -- for
example: authorization checks in a RAP behavior definition (DCL --
Data Control Language), early numbering vs. late numbering for key
generation, unmanaged vs. managed business objects, or exposing a
service via OData V2 vs. V4 -- and explain it below in your own words,
as if teaching a classmate who knows classic ABAP but has never
touched RAP.

## CONCEPT CHOSEN

Unmanaged vs. managed RAP business objects (who is responsible for
persistence).

## MY EXPLANATION (write this BEFORE looking anything up)

In a MANAGED RAP business object, the framework itself handles all the
CRUD persistence -- when you define standard operations (create,
update, delete) in the behavior definition without writing your own
implementation for them, RAP generates the INSERT/UPDATE/DELETE
against the underlying database table for you, and your custom ABAP
code only needs to fill in the business logic on top (validations,
determinations, actions). In an UNMANAGED business object, RAP gives
you the framework's lifecycle hooks (the same behavior definition
structure, the same draft/transactional-buffer machinery if you want
it) but YOU write the actual persistence code yourself inside the
behavior pool's `save` method -- RAP calls your code at the right
points in the save sequence, but never touches the database directly
on your behalf. Managed is the default choice for a straightforward
table-backed object; unmanaged exists for cases where persistence
isn't a simple 1:1 table write -- wrapping an older BAPI, writing to
multiple tables in a specific non-obvious order, or replicating to a
non-ABAP system.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I initially assumed "unmanaged" meant you lose the RAP framework's
other conveniences too (draft handling, standard operations wiring,
Fiori Elements integration) and have to build everything by hand --
that's not right. Unmanaged only changes who writes the SAVE logic;
you still get the same behavior definition syntax, the same
determinations/validations/actions model, and can still use draft
handling on top of an unmanaged object. The part that's genuinely
fuzzy for me still is exactly which lifecycle method calls
(`earlynumbering_create`, `save`, `cleanup`, etc.) fire in what order
for an unmanaged object versus a managed one -- I understand the
concept but haven't yet traced a real unmanaged implementation
end-to-end to see the hooks fire.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

My order-entry app's core order/order-item objects are a clean fit for
MANAGED (plain table-backed CRUD, nothing unusual about how a save
happens), so I'm keeping those managed. If I add the "sync order to
an external shipping partner" feature I've been sketching, that
persistence step (calling an outbound service alongside the DB write,
possibly needing custom rollback/error handling if the external call
fails) is exactly the kind of non-trivial save logic that would push
me toward an unmanaged (or managed-with-unmanaged-save-override)
object instead.
