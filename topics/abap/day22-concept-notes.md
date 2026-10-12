# Day 22, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-21 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21 see your Day 21 file.)

## THE TASK

Pick ONE concept -- suggestions: CDS table functions (AMDP), the RAP
generator, factory actions, static actions, `with additional save`,
CDS parameters / parameterised views, or RAP BO test doubles -- and
explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

CDS table functions implemented with AMDP (ABAP Managed Database Procedures).

## MY EXPLANATION (write this BEFORE looking anything up)

A normal CDS view entity is defined in CDS SQL and the database turns it into a SELECT. Sometimes that is not expressive enough: you want database-specific SQL, such as window functions, hierarchies or SQLScript on SAP HANA, or you want to push a heavy calculation down to the database instead of looping over rows in ABAP. A CDS table function is the bridge. You declare it in CDS with `define table function ZI_Something returns { ... }`, giving the output fields with their types, and you point it at an ABAP implementation with `implemented by method zcl_amdp_something=>get_data`.

The implementing class is an AMDP class: it implements the marker interface `if_amdp_marker_hdb` and the method is declared `FOR TABLE FUNCTION zi_something` and written `BY DATABASE FUNCTION FOR HDB LANGUAGE SQLSCRIPT OPTIONS READ-ONLY USING <tables>`. Inside the body you write SQLScript, returning a table whose columns match the declared output. The `USING` clause lists the database tables or views the code touches, so the dependency is known to the ABAP system. For classic ABAP people: it is like a native SQL block (`EXEC SQL`) but typed, transported and checked, and the result can then be consumed like any other CDS entity, by other CDS views, in a RAP BO as the data source of a query, or by `SELECT` in ABAP. Client handling is explicit: if the function is client-dependent you declare `with parameters @Environment.systemField: #CLIENT p_clnt : abap.clnt` and filter on it yourself.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Table functions are read-only and are tied to the HANA database, so they are not portable to other databases. They are also a last resort: prefer plain CDS view entities, which the optimizer can push down and which are database independent, and use a table function only when you really need SQLScript. A table function cannot be the base of a managed read-write BO directly: for changes you still need an unmanaged BO or a separate write path. I first thought they ran in the ABAP application server, but the code executes entirely in the database.
