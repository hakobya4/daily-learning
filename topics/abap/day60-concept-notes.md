# Day 60, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: ABAP Managed Database Procedures (AMDP: `IF_AMDP_MARKER_HDB`, `BY DATABASE PROCEDURE FOR HDB LANGUAGE SQLSCRIPT OPTIONS READ-ONLY USING ...`, why every table must be listed in `USING`, how importing/exporting parameters map to SQLScript table variables, and when "code pushdown" with AMDP is worth it compared to plain ABAP SQL or a CDS view), CDS table functions (`define table function ... returns { ... } implemented by method cl=>m`, the `FOR TABLE FUNCTION` AMDP method, and the client-handling annotation `@ClientHandling.type` / `.algorithm`), or modern ABAP SQL features (common table expressions `WITH +cte AS ( ... )`, `UNION` / `INTERSECT` / `EXCEPT`, window expressions `OVER( PARTITION BY ... )`, host expressions `@( ... )`, and `SELECT ... FROM @itab` to query an internal table) -- and explain it as if teaching a classmate who knows classic ABAP report programs and `SELECT ... ENDSELECT` but has never pushed logic down to the database.

## CONCEPT CHOSEN

TODO: name the concept.

## MY EXPLANATION (write this BEFORE looking anything up)

TODO: explain it in your own words -- what problem it solves, how it works, and when you would (and would not) use it.

## A SMALL EXAMPLE

```abap
* TODO: a short, self-written code snippet that shows the concept in action
```

## WHAT I GOT WRONG / CHECKED AFTERWARDS

TODO: after writing the explanation, check it against SAP Help / the ABAP keyword documentation and note anything you corrected.

## ONE-LINE TAKEAWAY

TODO
