# Day 56, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: class-based exceptions (`CX_STATIC_CHECK` vs. `CX_DYNAMIC_CHECK` vs. `CX_NO_CHECK`, what the compiler enforces for each with `RAISING`, `RAISE EXCEPTION NEW ...`, `TRY ... CATCH ... CLEANUP`, `RETRY` / `RESUME` with `RAISE RESUMABLE EXCEPTION`, and attaching T100 message texts via `IF_T100_MESSAGE` / `IF_T100_DYN_MSG` and `MESSAGE` in the `RAISE` statement), change documents (change document objects in SCDO, the generated `*_WRITE_DOCUMENT` function module, `CDHDR` / `CDPOS`, and when you would use them instead of a hand-made history table), or grouping internal tables with `LOOP AT ... GROUP BY` (group keys, `WITHOUT MEMBERS`, `LOOP AT GROUP`, `REDUCE` / `FOR GROUPS` in constructor expressions, and how it replaces the classic `AT NEW` / `AT END OF` control-level processing) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP or modern ABAP syntax.

## CONCEPT CHOSEN

Grouping internal tables with `LOOP AT ... GROUP BY` (group keys, `WITHOUT MEMBERS`, `LOOP AT GROUP`, `FOR GROUPS` / `REDUCE`) and how it replaces classic `AT NEW` / `AT END OF` control-level processing.

## MY EXPLANATION (write this BEFORE looking anything up)

In a classic report, if you wanted totals per customer you'd `SORT` the itab by customer, then `LOOP AT` it and use `AT NEW kunnr` / `AT END OF kunnr` / `SUM` to detect where a group starts and ends. That works, but it is fragile: it only looks at the field *position* in the line (everything left of the control field counts too), the work area's fields to the right get blanked to `*` inside the control blocks, and if you forget to sort first you silently get wrong groups.

`LOOP AT itab INTO DATA(wa) GROUP BY key` does the grouping for you, with no sorting needed. The loop body runs once **per group**, not once per row. The key can be one field (`GROUP BY wa-kunnr`) or a structure built on the fly (`GROUP BY ( kunnr = wa-kunnr year = wa-gjahr )`), and it can even be computed (`GROUP BY ( big = xsdbool( wa-amount > 1000 ) )`). You can also ask for `size = GROUP SIZE` and `index = GROUP INDEX` inside the key. Add `INTO DATA(grp)` / `REFERENCE INTO DATA(grp)` to name the group, and the group key is reachable through it.

Inside the group loop you visit the rows of that group with a nested `LOOP AT GROUP grp INTO DATA(member)`. That is where you'd do what `SUM` / `AT END OF` used to do:

```abap
LOOP AT lt_items INTO DATA(item)
     GROUP BY ( customer = item-kunnr  count = GROUP SIZE )
     ASCENDING
     INTO DATA(cust).
  DATA(total) = REDUCE wrbtr( INIT s = 0
                              FOR m IN GROUP cust
                              NEXT s = s + m-amount ).
  WRITE: / cust-customer, cust-count, total.
ENDLOOP.
```

`ASCENDING` / `DESCENDING` sorts the groups by their key. `WITHOUT MEMBERS` says "I only need the keys" (for example a distinct list of customers). It's cheaper, but then `LOOP AT GROUP` isn't allowed. The same grouping works in constructor expressions: `VALUE #( FOR GROUPS g OF wa IN itab GROUP BY wa-kunnr ( g ) )` builds a table of distinct keys in one statement, and `FOR m IN GROUP g` inside a `REDUCE` or `VALUE` aggregates per group.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

I wrongly assumed `GROUP BY` behaves like SQL and needs an aggregate function. In ABAP there is no implicit `SUM`, so you aggregate yourself, either with `LOOP AT GROUP` or with `REDUCE ... FOR m IN GROUP g`. I also thought the groups come out sorted. Without `ASCENDING`/`DESCENDING` they come out in the order in which each key is **first encountered** in the table, which is still deterministic but is not sorted. One subtle point: by default (the "representative binding") the work area `item` holds the *first row* of the current group inside the outer loop. Once you add `INTO grp` you get "group key binding", and you should use `grp` / `grp-customer` instead of relying on `item`. Finally, `GROUP BY` is not limited to adjacent rows, because rows with the same key anywhere in the table end up in the same group. That is the big practical difference from `AT NEW`, which only reacts to changes between neighbouring rows and is why the classic version needs the `SORT` first.
