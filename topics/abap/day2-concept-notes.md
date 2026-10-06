# Day 2, Task 9 -- ABAP/RAP: explain one concept in your own words

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project -- for example: CDS views, behavior definitions,
managed vs. unmanaged BOs, draft handling, or an OData service
exposure -- and explain it below IN YOUR OWN WORDS, as if teaching a
classmate who knows classic ABAP but has never touched RAP.

This is active recall: writing it out from memory (then checking a
reference afterward to correct yourself) sticks far better than just
rereading documentation.

## CONCEPT CHOSEN

CDS views (Core Data Services views) in the RAP model.

## MY EXPLANATION (write this BEFORE looking anything up)

A CDS view is a database view defined in the data dictionary layer using a SQL-like DDL, but it lives in the ABAP server and can carry extra semantics through annotations and associations. Instead of writing SELECTs with joins in ABAP code, I declare the data model once: which tables to read, how they relate (associations), and which fields are keys, amounts or texts. In RAP, CDS views form the layers of the business object: a root view entity describes the data, a projection view exposes only what a given service needs, and the behavior definition is attached to the root. Because the logic sits in the database layer, the work is pushed down to the database (code-to-data) rather than pulling rows into ABAP and looping over them.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I was fuzzy on the difference between a classic CDS view (DEFINE VIEW) and a view entity (DEFINE VIEW ENTITY): RAP uses view entities, which need no separate SQL view object and are the recommended modern form. I also mixed up the interface view and projection view roles: the interface layer is the stable reusable model, while projection views tailor it per consumer/service, adding UI annotations. Associations are not joins: they are resolved lazily, only when a path expression uses them.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio project I will define a root view entity for the main business object, a child entity composed to it, and a projection layer annotated for a Fiori Elements list report, then expose it as an OData service.
