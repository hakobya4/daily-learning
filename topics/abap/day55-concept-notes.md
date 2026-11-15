# Day 55, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: CDS hierarchies (`DEFINE HIERARCHY` over a parent-child association, `SOURCE ... CHILD TO PARENT ASSOCIATION ... START WHERE`, the generated `$node` / hierarchy attributes like `HIERARCHY_LEVEL`, and why this beats a hand-written recursive loop over a self-referencing table), the Background Processing Framework (bgPF -- running work asynchronously and transactionally after `COMMIT WORK` / from a RAP save sequence, controlled vs. uncontrolled operations, and what it replaces from the classic `CALL FUNCTION ... IN BACKGROUND TASK` world), or internal table kinds and secondary keys (STANDARD vs. SORTED vs. HASHED tables, `WITH UNIQUE/NON-UNIQUE KEY`, adding a `SECONDARY KEY` and reading `USING KEY`, and the cost model of each access) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP or modern ABAP syntax.

## CONCEPT CHOSEN

Internal table kinds (STANDARD vs. SORTED vs. HASHED), their primary keys, and secondary keys (`WITH ... SECONDARY KEY`, reading `USING KEY`) -- and the cost of each kind of access.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic report programs most of us declared every internal table as `TYPE STANDARD TABLE OF ... WITH DEFAULT KEY` (or the old `OCCURS 0` / `TABLES` style) and then wrote `READ TABLE itab WITH KEY ...`. That works, but it hides the fact that ABAP has three table kinds with very different performance, and that the key you declare is part of the contract.

**STANDARD table** -- an array in insertion order. Access by index (`itab[ 5 ]`) is O(1). Access by key (`READ TABLE ... WITH KEY matnr = ...` or `itab[ matnr = ... ]`) is a **linear search**, O(n), unless you `SORT` it yourself and add `BINARY SEARCH` (O(log n), but then *you* are responsible for keeping it sorted, and forgetting is a classic bug). The primary key of a standard table is always NON-UNIQUE, and `WITH DEFAULT KEY` means "all character-like fields of the line", which is almost never what you want -- better `WITH EMPTY KEY` or an explicit key.

**SORTED table** -- the system keeps lines sorted by the primary key at all times. You declare `WITH UNIQUE KEY` or `WITH NON-UNIQUE KEY`. Key reads use a binary search automatically (O(log n)), and -- the big one -- `LOOP AT itab WHERE <leading part of the key> = ...` is optimised: the kernel jumps to the first matching line instead of scanning everything. Index access still works. Inserting costs O(log n) to find the position (plus shifting), and you cannot `APPEND` out of order or `SORT` a sorted table by something else (runtime error / syntax error).

**HASHED table** -- lines are found through a hash of the key. The key MUST be `UNIQUE`. A read with the FULL key is O(1) on average regardless of size, which makes hashed tables the right choice for big lookup buffers ("customer number -> customer data" read thousands of times in a loop). There is no index access (`itab[ 3 ]` is not allowed), a partial key does not use the hash (falls back to a full scan), and `LOOP AT ... WHERE` is always a full scan.

**Secondary keys** solve the problem "I need fast access by more than one field combination". You add them in the type declaration:

```abap
TYPES ty_orders TYPE SORTED TABLE OF zorder
      WITH UNIQUE KEY primary_key COMPONENTS order_id
      WITH NON-UNIQUE SORTED KEY by_customer COMPONENTS customer_id order_date
      WITH UNIQUE HASHED KEY by_ext_ref COMPONENTS external_ref.

DATA orders TYPE ty_orders.

" primary key (implicit):
DATA(o1) = orders[ order_id = '4711' ].
" secondary keys must be named explicitly:
DATA(o2) = orders[ KEY by_ext_ref external_ref = 'PO-99' ].
LOOP AT orders INTO DATA(o) USING KEY by_customer WHERE customer_id = '1000'.
  ...
ENDLOOP.
READ TABLE orders INTO o WITH KEY by_customer COMPONENTS customer_id = '1000'.
```

A secondary key can be SORTED (unique or non-unique) or HASHED (unique only), independent of the table kind -- you can even put secondary keys on a STANDARD table. The system maintains the secondary index for you; you just have to say `USING KEY` / `KEY name` in the statement, otherwise the primary key (or a full scan) is used. Unique secondary keys are checked immediately on insert (a duplicate makes `INSERT` fail with `sy-subrc = 4`, or a short dump for some statements), while non-unique sorted secondary keys are updated *lazily* -- the index is (re)built the first time you actually use that key after changes.

The cost model I keep in my head:

| access                                 | STANDARD          | SORTED      | HASHED          |
|----------------------------------------|-------------------|-------------|-----------------|
| by index                               | O(1)              | O(1)        | not possible    |
| read by full key                       | O(n) (O(log n) with BINARY SEARCH on a sorted copy) | O(log n) | O(1) |
| `LOOP ... WHERE` leading key fields     | O(n)              | O(log n + k)| O(n)            |
| insert                                 | O(1) append       | O(log n) + shift | O(1)       |

Secondary keys are not free: each one costs memory and update time on every insert/delete/modify, so they pay off for tables that are filled once and read many times by different criteria, not for tables that are constantly changed and read once.

Rule of thumb I would tell a classmate: small tables (a few dozen lines) -- standard is fine. Big table, read by one unique key -- HASHED. Big table, read by key ranges or partial keys, or you need it ordered anyway -- SORTED. Need a second access path -- add a secondary key instead of keeping a sorted copy of the table yourself.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- I had to double-check the lazy update rule: it applies to NON-UNIQUE secondary keys only. Unique secondary keys (sorted or hashed) are updated immediately because uniqueness has to be checked on every insert -- so a duplicate value is rejected right away, not later.
- `itab[ ... ]` table expressions raise the exception `CX_SY_ITAB_LINE_NOT_FOUND` when nothing matches, while `READ TABLE` just sets `sy-subrc = 4`. So when I switch old `READ TABLE` code to table expressions I need `VALUE #( itab[ ... ] OPTIONAL )`, `DEFAULT`, `line_exists( )` or a `TRY` block.
- The name `primary_key` is predefined: I can write `USING KEY primary_key` to be explicit, and I can give the primary key an alias name in the declaration -- but I cannot name a secondary key `primary_key`.
- Inside a `LOOP ... USING KEY by_customer`, modifying a component of the key being looped over is forbidden (runtime error), the same as changing primary key fields of a sorted/hashed table -- `MODIFY` with key fields only works on standard tables.
- `DELETE ADJACENT DUPLICATES` and `SORT` also accept `USING KEY`, which I did not know; and for STANDARD tables a plain key read (no `BINARY SEARCH`, no secondary key) really is a full linear scan, so the "forgot to sort" bug is not just slow but can return the wrong line with `BINARY SEARCH` on an unsorted table.
