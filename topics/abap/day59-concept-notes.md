# Day 59, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: ABAP Unit with test doubles (`FOR TESTING` classes, `RISK LEVEL` / `DURATION`, `setup` / `teardown` / `class_setup`, `cl_abap_unit_assert`, dependency injection through interfaces vs. `TEST-SEAM` / `TEST-INJECTION`, `cl_abap_testdouble=>create` + `configure_call`, and the ABAP SQL / CDS test double frameworks `cl_osql_test_environment` and `cl_cds_test_environment`), field symbols vs. data references (`ASSIGN` / `FIELD-SYMBOL( )` inline, `REF #( )`, `->*`, `CREATE DATA` with a dynamic type, `IS ASSIGNED` vs. `IS BOUND`, and why `LOOP AT ... ASSIGNING` beats `INTO` for changing large rows), or CDS view entities with associations (`define view entity`, `association [0..*] to ... as _Items on ...`, exposing associations, path expressions like `_Items._Product.Name`, filtered associations, and how they differ from classic joins and from the older DDIC-based CDS views) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP or modern ABAP syntax.

## CONCEPT CHOSEN

Field symbols vs. data references: `FIELD-SYMBOLS` / inline `FIELD-SYMBOL( )` with
`ASSIGN`, data references with `REF #( )` / `GET REFERENCE`, dereferencing with `->*`,
`CREATE DATA` with a dynamic type, `IS ASSIGNED` vs. `IS BOUND`, and why
`LOOP AT ... ASSIGNING` beats `LOOP AT ... INTO` when changing large rows.

## MY EXPLANATION (write this BEFORE looking anything up)

**The problem.** Classic ABAP works with *copies*: `READ TABLE itab INTO wa`, change `wa`,
then `MODIFY itab FROM wa`. For wide rows or big tables that is a lot of copying, and it is
easy to forget the `MODIFY`. And sometimes you don't even know at design time *which*
variable or *which type* you will work on (a component chosen by name, a table type that
comes from customizing). Both field symbols and data references solve this by letting you
work with "the original data object itself" instead of a copy.

**Field symbols = an alias / placeholder.** A field symbol has no memory of its own. After
`ASSIGN wa-matnr TO <fs>` (or `ASSIGN COMPONENT 'MATNR' OF STRUCTURE wa TO <fs>`, or
`LOOP AT itab ASSIGNING FIELD-SYMBOL(<row>)`, or `READ TABLE ... ASSIGNING <row>`), every
use of `<fs>` IS the assigned data object -- writing `<fs> = 42` writes into the original.
Think of it as a pointer that is automatically dereferenced: there is no "address" you can
store or pass around, you just use `<fs>` like a normal variable. It can be typed fully
(`TYPE mara`), generically (`TYPE any`, `TYPE ANY TABLE`, `TYPE data`), or by the inline
declaration that takes the type from the source. Before it is assigned (or after
`UNASSIGN`), using it dumps (`GETWA_NOT_ASSIGNED`), so you check `IS ASSIGNED`. A failed
dynamic `ASSIGN` sets `sy-subrc = 4` (newer releases also offer the addition
`ELSE UNASSIGN`) and leaves the field symbol as it was -- so always check.

**Data references = a real pointer value.** A reference variable (`DATA lr TYPE REF TO
mara` or `TYPE REF TO data`) holds the *address* of a data object as a value. You get one
with `lr = REF #( wa )` (old style: `GET REFERENCE OF wa INTO lr`), or by asking the system
for new memory with `CREATE DATA lr TYPE mara` / `CREATE DATA lr TYPE (lv_type_name)` /
`CREATE DATA lr TYPE HANDLE lo_rtti_type` / `NEW #( )`. You dereference with `lr->*` (whole
object) or `lr->matnr` (component, for structured references). Because the reference is an
ordinary value, you can store it in an attribute, put many of them in an internal table,
pass it to a method, return it -- things a field symbol cannot do. A reference that points
nowhere is "initial"; you check with `IS BOUND` (`IS NOT INITIAL` only tells you it has a
value, `IS BOUND` that it points to a valid object). Data created with `CREATE DATA` lives
on the heap until no reference points to it any more (garbage collector), while a
reference to a *local* variable becomes invalid when the method ends.

**How they work together.** Generic `REF TO data` cannot be used directly in most
statements because the compiler doesn't know the type, so the typical dynamic pattern is
"create with a reference, work with a field symbol":

`CREATE DATA lr_tab TYPE STANDARD TABLE OF (lv_tabname). ASSIGN lr_tab->* TO <lt_tab>.
SELECT * FROM (lv_tabname) INTO TABLE @<lt_tab> UP TO 10 ROWS.`

**Why `ASSIGNING` beats `INTO` for changing rows.** `LOOP AT itab INTO wa` copies every
row into `wa` (cost grows with the row width), and your change to `wa` is lost unless you
`MODIFY itab FROM wa` (another copy plus a lookup). `LOOP AT itab ASSIGNING <row>` copies
nothing -- `<row>` points at the row in the table, `<row>-status = 'X'` changes it in place.
For sorted/hashed tables you must not change key fields through it (runtime error), which
is a useful safety net. `REFERENCE INTO lr_row` is the reference flavour of the same idea,
handy if you want to keep the row references afterwards. For narrow rows that you only
*read* (a couple of short fields), `INTO` is fine and sometimes clearer -- the difference
only matters for wide rows or big tables.

**When to use which.** Field symbol: local, short-lived access -- loops, `READ TABLE`,
dynamic component access (`ASSIGN COMPONENT`), working with generically typed data inside
one method. Data reference: when the "pointer" must outlive the statement -- stored in
an attribute or table, passed between methods, or when you must *create* data of a type
known only at runtime. Avoid both when a plain typed variable does the job: dynamic code is
harder to read, can't be checked by the syntax check, and fails at runtime instead.

## A SMALL EXAMPLE

```abap
REPORT zday59_fs_vs_ref.

TYPES: BEGIN OF ty_order,
         id     TYPE i,
         amount TYPE p LENGTH 10 DECIMALS 2,
         status TYPE c LENGTH 1,
         text   TYPE c LENGTH 1000,   " wide row: copying it is not free
       END OF ty_order,
       tt_order TYPE STANDARD TABLE OF ty_order WITH EMPTY KEY.

DATA(orders) = VALUE tt_order( ( id = 1 amount = '120.00' )
                               ( id = 2 amount = '15.50' )
                               ( id = 3 amount = '980.00' ) ).

" 1) Field symbol: change rows in place, no MODIFY needed
LOOP AT orders ASSIGNING FIELD-SYMBOL(<order>).
  <order>-status = COND #( WHEN <order>-amount > 100 THEN 'B' ELSE 'S' ).
ENDLOOP.

" 2) Dynamic component access by name
ASSIGN COMPONENT 'AMOUNT' OF STRUCTURE orders[ 1 ] TO FIELD-SYMBOL(<value>).
IF <value> IS ASSIGNED.
  <value> = <value> * 2.                       " orders[ 1 ]-amount is now 240.00
ENDIF.

" 3) Data references: keep pointers to the big orders for later
DATA big_orders TYPE STANDARD TABLE OF REF TO ty_order WITH EMPTY KEY.
LOOP AT orders REFERENCE INTO DATA(order_ref) WHERE status = 'B'.
  APPEND order_ref TO big_orders.
ENDLOOP.
LOOP AT big_orders INTO DATA(ref).
  ref->status = 'R'.                           " changes the row inside ORDERS
ENDLOOP.

" 4) CREATE DATA with a type known only at runtime + field symbol to use it
DATA(type_name) = `TT_ORDER`.                  " could come from customizing
DATA dyn_ref TYPE REF TO data.
CREATE DATA dyn_ref TYPE (type_name).
ASSIGN dyn_ref->* TO FIELD-SYMBOL(<dyn_table>).
IF dyn_ref IS BOUND AND <dyn_table> IS ASSIGNED.
  <dyn_table> = orders.                        " generic, but works: same type
  cl_demo_output=>display( <dyn_table> ).
ENDIF.
```

## WHAT I GOT WRONG / CHECKED AFTERWARDS

* I was not sure whether inline `FIELD-SYMBOL( )` in `ASSIGN COMPONENT` gets a concrete
  type -- it is typed generically (`TYPE data`) because the component is only known at
  runtime, so arithmetic on it works but the syntax check can't help you. Checked in the
  ABAP keyword documentation for `ASSIGN`, inline declarations.
* `IS BOUND` vs. `IS NOT INITIAL`: a data reference to a local variable of a method that
  has already returned is not initial but also not bound -- only `IS BOUND` catches that
  "dangling" case. I had first written that `IS NOT INITIAL` is enough.
* Changing key fields of a SORTED/HASHED table through `ASSIGNING` or a reference raises a
  runtime error (the key fields are write-protected) -- for STANDARD
  tables with an empty key (like above) it is allowed.
* `GET REFERENCE OF` still works but `REF #( )` is the modern form and can be used inline
  in expressions and method calls.
* The failed-`ASSIGN` behaviour: for dynamic `ASSIGN` variants `sy-subrc` is set and the
  field symbol keeps its previous state, so a reused `<fs>` may still point at the *old*
  data object -- an `UNASSIGN` (or the `ELSE UNASSIGN` addition on newer releases) before
  the dynamic `ASSIGN` avoids silently working on the wrong field.

## ONE-LINE TAKEAWAY

A field symbol is a dereferenced alias you use right now (`ASSIGNING` = change in place,
no copies); a data reference is a pointer *value* you can store, pass and create at
runtime (`REF #`, `CREATE DATA`, `->*`) -- check `IS ASSIGNED` for the one, `IS BOUND` for
the other, and combine them for dynamic programming.
