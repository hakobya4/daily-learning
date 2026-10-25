# Day 34, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-33 -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: CDS custom entities with a query
implementation class, `READ ENTITIES ... FIELDS` vs. `ALL FIELDS WITH`,
`FAILED` / `REPORTED` / `MAPPED` response structures, ABAP SQL aggregate
expressions and `GROUP BY`, constructor expressions (`VALUE`,
`CORRESPONDING`, `COND`, `REDUCE`), CDS view entity parameters, or the
clean-core / released-API idea -- and explain it as if teaching a
classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

ABAP constructor expressions: `VALUE`, `CORRESPONDING`, `COND` and `REDUCE`.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you build data with several statements: declare a work area, fill fields, APPEND it to a table. Constructor expressions let you create a value in one expression, right where you need it, using an operator followed by a type and parentheses.

- `VALUE type( ... )` builds a structure or internal table inline: `VALUE ty_line( id = 1 name = 'A' )` or `VALUE tt_lines( ( id = 1 ) ( id = 2 ) )`. Each inner pair of parentheses is one table row.
- `CORRESPONDING type( source )` copies fields with matching names from one structure or table into another type. `MAPPING` renames fields and `EXCEPT` skips some. This is what you use in RAP to move data between CDS entity structures and table structures.
- `COND type( WHEN cond1 THEN a WHEN cond2 THEN b ELSE c )` is an inline IF/ELSEIF that returns a value, so it can be used in an assignment or method call.
- `REDUCE type( INIT x = 0 FOR wa IN itab NEXT x = x + wa-amount )` loops over a table and accumulates one result, e.g. a sum, without a separate LOOP.

They matter in RAP because EML calls need structured input such as `MODIFY ENTITIES ... CREATE FROM VALUE #( ( %cid = 'c1' ... ) )`, and the `#` lets the compiler infer the type.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- `VALUE` with `FOR` loops can also build a table from another table. `REDUCE` needs `INIT` and `NEXT`, and the result type must match the accumulator. `CORRESPONDING` only copies same-named fields and does not convert deep structures unless `DEEP` is used.
