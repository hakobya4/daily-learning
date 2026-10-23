# Day 32, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-31 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-25 see your own files; Day 26 static
actions; Day 27 CDS associations vs. compositions; Day 28-31 see your
files.)

## THE TASK

Pick ONE concept -- suggestions: CDS parameters / parameterised views,
RAP BO test doubles (`cl_botd_...`), the RAP generator, `%control` /
`%tky` structures, `internal` actions, CDS extension views, ABAP Unit with
the SQL test double framework, `FOR ALL ENTRIES` vs. CDS joins, RAP
`determine action`, or CDS view entities vs. classic DDIC-based CDS views
-- and explain it as if teaching a classmate who knows classic ABAP but
has never touched RAP.

## CONCEPT CHOSEN

CDS view entities vs. classic DDIC-based CDS views.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you create a DDIC view or table in SE11. The old style of CDS (`define view` with `@AbapCatalog.sqlViewName`) is like that: every CDS view secretly generates a second object, an SQL view in the DDIC, with a name of up to 16 characters. So you had two names to maintain, the CDS name and the SQL view name, and the SQL view was what the database really saw.

A CDS view entity (`define view entity`) drops that second object. There is only the CDS entity itself, no `sqlViewName`, and the runtime creates the database view from it directly. It is the recommended and, for RAP, the required way to model data: in current RAP releases the base and projection views are view entities, and the old DDIC-based views are deprecated.

Compared with classic views: you remove `@AbapCatalog.sqlViewName` and `@AbapCatalog.compiler.compareFilter`, there is stricter syntax checking (for example, associations must be defined and used consistently and some implicit conversions are no longer silently allowed), better support for newer features (like parameters, session variables and extensions via `extend view entity`), and no more activation problems caused by name clashes on the SQL view. Think of it as the same SELECT-with-annotations idea in classic CDS, only without the DDIC middleman.

Migrating: it is mostly mechanical (change `define view` to `define view entity`, delete the SQL view annotation), but you must check use of `$projection`, casts and the `@ClientHandling` annotation, because view entities always handle the client automatically.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- I should not say "required" for every RAP case without caveats: view entities are the recommended and current standard, but existing DDIC-based views can still be read in older systems.
- Client handling is automatic in view entities, so `@ClientHandling` is no longer used; in the old views it controlled whether the client field was visible.
- Extending them uses `extend view entity`, not `extend view`; the two kinds of extension cannot be mixed.
- Migrating to a view entity changes the object type, so the old SQL view name stops existing; code that selected from the SQL view name directly (via native SQL or SE16) will break.
