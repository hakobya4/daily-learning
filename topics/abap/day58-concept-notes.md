# Day 58, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: class-based exceptions (`CX_STATIC_CHECK` vs. `CX_DYNAMIC_CHECK` vs. `CX_NO_CHECK`, the `RAISING` clause, `TRY ... CATCH ... CLEANUP`, `RAISE EXCEPTION TYPE ... EXPORTING`, `RETRY` / `RESUME` with `RAISE RESUMABLE EXCEPTION`, exception chaining with `previous`, and how all this differs from classic `EXCEPTIONS` / `sy-subrc` in function modules), the SALV object model for ALV output (`cl_salv_table=>factory`, columns / functions / sorts / aggregations objects, event handling for `double_click`, and why it replaced `REUSE_ALV_GRID_DISPLAY` for most reports), or lock objects and the SAP enqueue (`SE11` lock objects, the generated `ENQUEUE_` / `DEQUEUE_` function modules, lock modes `E` / `S` / `X` / `O`, `_SCOPE`, `_WAIT`, transaction `SM12`, and why a database lock alone is not enough across dialog steps) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP or modern ABAP syntax.

## CONCEPT CHOSEN

Class-based exceptions: `CX_STATIC_CHECK` vs. `CX_DYNAMIC_CHECK` vs. `CX_NO_CHECK`, the
`RAISING` clause, `TRY ... CATCH ... CLEANUP`, `RAISE EXCEPTION TYPE ... EXPORTING`,
`RETRY` / `RESUME` with `RAISE RESUMABLE EXCEPTION`, chaining with `previous` -- and how
this differs from classic `EXCEPTIONS` / `sy-subrc` in function modules.

## MY EXPLANATION (write this BEFORE looking anything up)

**The problem with the classic way.** A function module declares `EXCEPTIONS not_found
= 1 OTHERS = 2`, raises with `RAISE not_found` (or `MESSAGE ... RAISING not_found`) and
the caller has to check `sy-subrc` right after the call. Nothing forces the caller to
check it, the only information that travels is a number (plus maybe `sy-msgid/msgno`),
and if the caller does not list the exception in its `EXCEPTIONS` part, the program
dumps. You also cannot pass the error up through several call levels without every level
re-checking `sy-subrc` and re-raising by hand.

**Exceptions as objects.** In class-based exception handling an error is an *instance of
an exception class* (`ZCX_...`, ultimately inheriting from `CX_ROOT`). The object carries
real attributes (the order number that was not found, a text from a message class or an
OTR text via `IF_T100_MESSAGE` / `IF_T100_DYN_MSG`), `get_text( )` for the readable
message, and `previous` -- a reference to the exception that caused this one. You raise it
with

```
RAISE EXCEPTION TYPE zcx_order_not_found EXPORTING order_id = lv_id.
" or, 7.52+: RAISE EXCEPTION TYPE zcx_... MESSAGE e001(zorders) WITH lv_id.
" or as an expression: ... THROW zcx_order_not_found( order_id = lv_id ) inside COND/SWITCH
```

and it travels up the call stack automatically until a `TRY` block with a matching
`CATCH` is found -- matching by class *or any superclass*, so `CATCH cx_root` catches
everything and the order of `CATCH` clauses matters (most specific first).

**The three superclasses decide who must care.**

* `CX_STATIC_CHECK` -- a method that can let it escape MUST declare it in its `RAISING`
  clause, and the syntax check warns when you call such a method without catching or
  re-declaring it. Use it for *expected, business-level* errors the caller should handle
  ("order not found", "credit limit exceeded"). Most of your own `ZCX_` classes.
* `CX_DYNAMIC_CHECK` -- must also be declared in `RAISING` to leave a method, but the
  check happens only at runtime (no syntax warning). For errors that a careful caller can
  avoid in advance, e.g. `CX_SY_ZERODIVIDE`, `CX_SY_ITAB_LINE_NOT_FOUND` from a table
  expression `itab[ key = x ]` -- you either check first (`line_exists( )`) or catch.
* `CX_NO_CHECK` -- may leave any method without being declared; for things that can
  happen anywhere and that nobody can sensibly handle locally (resource exhaustion,
  `CX_SY_EXPORT_BUFFER_NO_MEMORY`-type situations, framework-level errors).

If an exception that violates the `RAISING` contract leaves a method (a static/dynamic
check exception not declared), it is converted to `CX_SY_NO_HANDLER` (with the original
in `previous`). If nobody catches at all, you get a short dump in ST22 that shows the
exception class and its text.

**TRY / CATCH / CLEANUP.**

* `CATCH zcx_a zcx_b INTO DATA(lx)` -- handle it; `lx->get_text( )` for the message.
* `CLEANUP` -- runs when an exception passes *through* this `TRY` block because it is
  caught somewhere further up; the place to release locks, close files, reset state.
  It does NOT run when the exception is caught in this same `TRY`, and you must not
  leave the block with `RETURN` etc. from inside it.
* `RETRY` (inside a `CATCH`) -- restart the whole `TRY` block from the beginning, e.g.
  after fixing a parameter or waiting for a lock. Needs a counter, otherwise endless loop.
* `RAISE RESUMABLE EXCEPTION TYPE ...` + `CATCH BEFORE UNWIND ...` + `RESUME` -- a
  resumable exception keeps the context of the raising method alive; the handler can
  decide "this is only a warning, carry on" and `RESUME` continues right after the
  `RAISE RESUMABLE` statement. This only works if every method on the way declares it as
  `RAISING RESUMABLE( zcx_... )`. Good for "collect warnings but keep processing"
  scenarios.

**Chaining with `previous`.** When a low-level error should be reported as a business
error, catch it and raise your own with `EXPORTING previous = lx_low`. The caller sees a
meaningful `ZCX_ORDER_SAVE_FAILED`, and the root cause is still available by walking
`previous`. Never just swallow the low-level exception.

**When (not) to use it.** All new methods and classes: class-based exceptions. Classic
`EXCEPTIONS` stay for calling existing function modules / BAPIs (and BAPIs don't raise at
all -- they return `BAPIRET2` messages in `RETURN`, which you still check yourself). The
two styles cannot be mixed in one procedure: a method with `RAISING` cannot also use
`EXCEPTIONS`, so when wrapping an old function module you catch `sy-subrc <> 0` and turn it
into `RAISE EXCEPTION TYPE zcx_...`. Do not use exceptions for normal control flow
(e.g. "loop until not found") -- they are comparatively expensive and hide the logic.

## A SMALL EXAMPLE

```abap
CLASS zcx_order_error DEFINITION PUBLIC INHERITING FROM cx_static_check.
  PUBLIC SECTION.
    INTERFACES if_t100_dyn_msg.
    DATA order_id TYPE vbeln READ-ONLY.
    METHODS constructor
      IMPORTING textid   LIKE if_t100_message=>t100key OPTIONAL
                previous LIKE previous OPTIONAL
                order_id TYPE vbeln OPTIONAL.
ENDCLASS.

CLASS zcx_order_error IMPLEMENTATION.
  METHOD constructor ##ADT_SUPPRESS_GENERATION.
    super->constructor( previous = previous ).
    me->order_id = order_id.
    if_t100_message~t100key = COND #( WHEN textid IS INITIAL
                                      THEN if_t100_message=>default_textid
                                      ELSE textid ).
  ENDMETHOD.
ENDCLASS.

CLASS lcl_orders DEFINITION.
  PUBLIC SECTION.
    METHODS get_net_value
      IMPORTING iv_id         TYPE vbeln
      RETURNING VALUE(rv_net) TYPE netwr_ak
      RAISING   zcx_order_error.
ENDCLASS.

CLASS lcl_orders IMPLEMENTATION.
  METHOD get_net_value.
    SELECT SINGLE netwr FROM vbak WHERE vbeln = @iv_id INTO @rv_net.
    IF sy-subrc <> 0.
      RAISE EXCEPTION TYPE zcx_order_error
        MESSAGE e001(zorders) WITH iv_id          " "Order &1 does not exist"
        EXPORTING order_id = iv_id.
    ENDIF.
  ENDMETHOD.
ENDCLASS.

DATA gt_items TYPE STANDARD TABLE OF vbap WITH EMPTY KEY.   " filled elsewhere

START-OF-SELECTION.
  DATA(lo_orders) = NEW lcl_orders( ).
  DATA(lv_tries)  = 0.
  DATA(lv_id)     = CONV vbeln( '12345' ).
  TRY.
      DATA(lv_net) = lo_orders->get_net_value( lv_id ).
      DATA(lv_avg) = lv_net / lines( gt_items ).   " may raise CX_SY_ZERODIVIDE
      WRITE: / |Net value { lv_net }, per item { lv_avg }|.
    CATCH zcx_order_error INTO DATA(lx_order).
      lv_tries += 1.
      IF lv_tries < 2.
        lv_id = |{ lv_id ALPHA = IN }|.           " fix the key (leading zeros) ...
        RETRY.                                     " ... and run the TRY block again
      ENDIF.
      MESSAGE lx_order TYPE 'S' DISPLAY LIKE 'E'.
    CATCH cx_sy_zerodivide INTO DATA(lx_div).
      WRITE: / lx_div->get_text( ).
  ENDTRY.
```

## WHAT I GOT WRONG / CHECKED AFTERWARDS

Checked against the ABAP keyword documentation (TRY, CATCH, CLEANUP, RAISE EXCEPTION,
RETRY, RESUME, exception classes):

* I first wrote that `CLEANUP` always runs "like `finally` in Java". Wrong: it runs only
  when the exception is NOT handled in this `TRY` but further up (or when the block is left
  early by certain statements). There is no `FINALLY` in ABAP.
* `RESUME` requires `CATCH BEFORE UNWIND`, otherwise the raising context has already been
  removed when the handler runs; and the exception must be raised with `RAISE RESUMABLE`
  and declared with `RAISING RESUMABLE( ... )` along the whole call chain -- an ordinary
  `RAISING` declaration makes it non-resumable for the caller.
* A violated `RAISING` contract yields `CX_SY_NO_HANDLER`, not an immediate dump -- it
  dumps only if that is not caught either.
* `MESSAGE ... ` addition on `RAISE EXCEPTION` and `IF_T100_DYN_MSG` exist from release
  7.50/7.52; on older systems the text has to be set via `textid` + attributes. The
  `THROW` operator in `COND`/`SWITCH` is 7.40 SP08+.
* Methods with `RAISING` and the classic `EXCEPTIONS` addition cannot be combined in one
  signature -- confirmed.

## ONE-LINE TAKEAWAY

Class-based exceptions turn errors from an easily-ignored `sy-subrc` number into typed
objects that the compiler (static check) makes callers deal with, carry their own text and
cause chain, and can be retried or even resumed.
