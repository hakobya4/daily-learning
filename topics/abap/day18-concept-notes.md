# Day 18, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-17 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent.)

## THE TASK

Pick ONE concept -- suggestions: the RAP BO test double framework,
CDS associations vs. compositions, projection views and behavior
projections, RAP business events, or the additional save / unmanaged save
in a managed BO -- and explain it as if teaching a classmate who knows
classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Projection views and behavior projections (CDS projection layer in RAP).

## MY EXPLANATION (write this BEFORE looking anything up)

Think of the RAP business object as a general-purpose, reusable core: a CDS data model (root view entity plus child entities) and a behavior definition holding all the business logic (determinations, validations, actions). A projection is a thin, service-specific "window" onto that core. In classic ABAP terms it is like exposing only some fields and some function modules of a big module to one particular caller.

A CDS projection view (`define root view entity ... as projection on ...`) selects which fields of the underlying view entity are visible, can rename them, and is where UI annotations and value helps live. A behavior projection (`projection;` in a behavior definition) then says which of the BO's operations (create, update, delete, actions, draft actions) this service reuses with `use create; use update; use action ...;`. It cannot add new business logic; it only exposes or hides what the base BO has.

Why it matters: one BO can serve several consumers (a Fiori app for clerks, one for managers, an API) with different fields and allowed operations, without duplicating the logic. The service definition then exposes the projection views, and a service binding publishes them (OData V2/V4 UI or Web API).

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- A projection can restrict operations but never widen them: you can only `use` what the base behavior defines (apart from a few projection-level options such as `use etag` and `use draft` alignment).
- The projection behavior definition must itself be consistent with the base: for draft BOs the projection has to expose the draft actions too (`use action Edit; use action Activate; ...`).
- Fields are exposed by listing them in the projection select list; anything not listed is invisible to that service, so authorization and sensitive fields are handled by simply leaving them out.
- Projections are what service definitions expose, not the base entities, which keeps the core model stable when a UI changes.
