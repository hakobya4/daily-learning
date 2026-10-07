# Day 16, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-15 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML.)

## THE TASK

Pick ONE concept -- suggestions: virtual elements in CDS, the RAP BO test
double framework, CDS associations vs. compositions, projection views and
behavior projections, `lock master` / `lock dependent`, or RAP
business events -- and explain it as if teaching a classmate who knows
classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Virtual elements in CDS (calculated at read time by an ABAP class).

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP, if a report needed a value that was not stored in a
table (say, days since an order was created, or a price converted at
today's rate), you just computed it in a loop after the SELECT. In a
RAP/CDS world the read is often pushed down to the database, and the
CDS view can only use what SQL can express. A virtual element is a field
that is declared in a CDS projection/consumption view with the
annotation `@ObjectModel.virtualElement: true` plus
`@ObjectModel.virtualElementCalculatedBy: 'ABAP:ZCL_MY_CALC'`, but has no
column behind it. The database never sees it. After the framework has
read the real data, it calls my ABAP class, which implements
`IF_SADL_EXIT_CALC_ELEMENT_READ`, once per result set. The class has two
methods: `get_calculation_info` tells the framework which real fields it
needs (so they are always selected) and `calculate` receives the rows and
fills in the virtual field for each of them.

Think of it as a callback or user exit on the read side: the field looks
like any other element to the OData service and the Fiori UI, but its
value comes from ABAP code. Good for things SQL cannot do (calling a
function module, complex rules). The cost is that the value cannot be
used for filtering or sorting on the database, since it does not exist
there, and the code must handle many rows at once, not one at a time.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Checks against my own understanding: the interface is
`IF_SADL_EXIT_CALC_ELEMENT_READ`, and virtual elements normally belong in
the projection layer. The main limitation to remember is that filtering,
sorting and aggregation on a virtual element are not pushed to the
database, so it should not be used where that is needed; if SQL can
express the value, a normal CDS expression is better. (Written without
live system access, so verify the exact annotation spelling in an ADT
project.)
