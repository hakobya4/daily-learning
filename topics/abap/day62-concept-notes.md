# Day 62, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: Business Add-Ins (BAdIs) in the enhancement framework (enhancement spots and BAdI definitions in SE18/SE20, `GET BADI` / `CALL BADI`, single- vs. multiple-use BAdIs, filter values, the fallback class, and why this beats the old user exits / `CL_EXITHANDLER` classic BAdIs and modifying SAP code), ABAP Channels (ABAP Messaging Channels with `cl_amc_channel_manager=>create_message_producer` and consumers that `RECEIVE MESSAGES` vs. ABAP Push Channels over WebSocket with `if_apc_wsp_extension`, and what problem "push instead of poll" solves for a Fiori app or between application servers), or ABAP Daemons (`cl_abap_daemon_ext_base`, `on_accept` / `on_start` / `on_message` / `on_error`, starting and stopping a daemon with `cl_abap_daemon_client_manager`, and when a long-lived background session is better than a periodic batch job) -- and explain it as if teaching a classmate who knows classic ABAP report programs, internal tables and `SELECT`, but has never used this feature.

## CONCEPT CHOSEN

Business Add-Ins (BAdIs) in the enhancement framework: enhancement spots and BAdI definitions (SE18), enhancement implementations and BAdI implementations (SE19), `GET BADI` / `CALL BADI`, single- vs. multiple-use BAdIs, filter values, the fallback class, and why this replaces user exits, classic BAdIs (`CL_EXITHANDLER`) and modifications.

## MY EXPLANATION (write this BEFORE looking anything up)

**The problem.** SAP ships standard code, every customer wants it to behave a little differently ("also check the credit limit", "fill this custom field", "send the order to our warehouse system"). Changing SAP's own code is a *modification*: it has to be re-checked and re-applied (SPAU) after every upgrade or support package. SAP's answer is to leave deliberate, documented **hooks** in its code where customer code can plug in without touching the original. Over the years these were form-based *user exits* (`USEREXIT_...` FORMs in SAP includes -- still a modification-ish thing), *customer exits* (CMOD/SMOD function modules `EXIT_...`), then *classic BAdIs* (object-oriented, instantiated with `CL_EXITHANDLER=>GET_INSTANCE`), and finally the **new (kernel) BAdIs** of the enhancement framework, which is what people mean today.

**The idea.** A BAdI is an **interface plus a call point**:
- The *provider* (SAP, or you, if you build a reusable application) defines a **BAdI definition** inside an **enhancement spot** (SE18 / SE80). The definition names a BAdI interface (methods with typed parameters), whether it is **single-use** or **multiple-use**, optional **filters**, and an optional **fallback class**.
- In the code, the provider writes two statements: `GET BADI lo_badi [FILTERS ...]` to obtain a *BAdI handle*, and `CALL BADI lo_badi->method( ... )` to call it. That's the whole hook.
- A *consumer* (the customer) creates an **enhancement implementation** (SE19) for that spot, containing a **BAdI implementation**: a class that implements the BAdI interface, plus its filter values and an active/inactive switch. No SAP object is changed; the implementation is the customer's own repository object, upgrade-safe, and can be switched via the Switch Framework.

**Single vs. multiple use.** *Multiple-use*: any number of implementations can be active; `CALL BADI` calls them **all**, one after another (order not guaranteed unless you use sorting via the "BAdI sorter" / sort criteria). Typical for "notify / enrich" hooks, so such methods usually have no RETURNING parameter -- whose result would win? *Single-use*: **exactly one** implementation is used; if none is active, the **fallback class** (defined with the BAdI) runs, which is how the provider ships default behaviour. If a single-use BAdI has neither an active implementation nor a fallback, `GET BADI` raises `CX_BADI_NOT_IMPLEMENTED`; with more than one active one you get `CX_BADI_MULTIPLY_IMPLEMENTED`. (A multiple-use BAdI with zero implementations is fine -- the call simply does nothing.)

**Filters.** A BAdI can declare filter characteristics (e.g. `COUNTRY TYPE land1`, `DOC_TYPE`). Each implementation states for which values it applies (conditions like `= 'DE'`, ranges, patterns). At runtime the provider passes the actual values: `GET BADI lo_badi FILTERS country = lv_land1.` and only the matching implementations end up in the handle. This lets one hook carry separate, cleanly separated implementations per country / company code / document type instead of one giant `CASE` in one exit.

**Why it beats the older techniques.** (1) Speed and simplicity: `GET BADI`/`CALL BADI` are kernel statements; the set of implementations is resolved by the kernel and buffered, while classic BAdIs went through `CL_EXITHANDLER` and dynamic instantiation every time. (2) It's checked statically: the interface is typed, the syntax check sees `CALL BADI` parameters. (3) It's upgrade-safe and transportable as the customer's own objects -- no SPAU work like for modifications or code inside SAP includes. (4) Multiple implementations from different teams/add-ons coexist (customer exits allowed only one project to own an exit). (5) Filters, fallback class, Switch Framework integration, and in ABAP Cloud "released" BAdIs are *the* supported extension mechanism -- you can't modify SAP code there at all.

**When to use / not.** Use a BAdI whenever SAP offers one at the point you need (search via the enhancement spot of the application, `SE84`/`SE18`, or breakpoints on `GET BADI` / `cl_badi_*` while running the transaction), and define your **own** BAdIs in your reusable applications when you want other teams or countries to plug in without editing your code. Don't use a BAdI as a general-purpose dependency-injection framework inside a single program (a plain interface + factory is simpler), don't put heavy logic or `COMMIT WORK` inside BAdI methods that run in the middle of a SAP update, and don't reach for implicit/explicit enhancement points (source-code plug-ins) if a proper BAdI exists -- those are much closer to modifications.

## A SMALL EXAMPLE

```abap
*----------------------------------------------------------------------*
* PROVIDER side: our own reusable order-check application.
* SE18: enhancement spot ZES_ORDER_CHECKS with BAdI definition
*       ZBADI_ORDER_CHECK, multiple-use, filter COUNTRY TYPE land1,
*       interface ZIF_BADI_ORDER_CHECK:
*----------------------------------------------------------------------*
INTERFACE zif_badi_order_check PUBLIC.
  INTERFACES if_badi_interface.                     " marks it as a BAdI interface
  METHODS check
    IMPORTING is_order    TYPE zorder_header
    CHANGING  ct_messages TYPE bapiret2_t.          " each implementation may add messages
ENDINTERFACE.

* ... in the provider's check method:
METHOD run_checks.
  DATA lo_badi TYPE REF TO zbadi_order_check.        " the type is the BAdI definition itself

  TRY.
      GET BADI lo_badi
        FILTERS
          country = is_order-country.                 " only implementations for this country
    CATCH cx_badi_not_implemented.                    " only possible for single-use BAdIs,
      RETURN.                                         " kept here for safety
  ENDTRY.

  CALL BADI lo_badi->check                            " calls ALL active, matching implementations
    EXPORTING is_order    = is_order
    CHANGING  ct_messages = rt_messages.
ENDMETHOD.

*----------------------------------------------------------------------*
* CONSUMER side: SE19 enhancement implementation ZEI_ORDER_CHECKS_DE,
* BAdI implementation ZBI_ORDER_CHECK_DE, filter COUNTRY = 'DE',
* implementing class:
*----------------------------------------------------------------------*
CLASS zcl_order_check_de DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_order_check.
ENDCLASS.

CLASS zcl_order_check_de IMPLEMENTATION.
  METHOD zif_badi_order_check~check.
    IF is_order-vat_id IS INITIAL.
      APPEND VALUE #( type = 'E' id = 'ZORDER' number = '010'
                      message = 'German orders need a VAT ID' ) TO ct_messages.
    ENDIF.
  ENDMETHOD.
ENDCLASS.
```

For a **single-use** variant (e.g. `ZBADI_ORDER_NUMBER` with `METHODS next_number RETURNING VALUE(rv) TYPE zorder_no`) you would tick "single use" in SE18 and give the definition a **fallback class** that implements the default numbering; a customer implementation then *replaces* it, and `GET BADI` never fails.

## WHAT I GOT WRONG / CHECKED AFTERWARDS

- I first thought `CALL BADI` on a multiple-use BAdI with no implementation would raise an exception -- it doesn't; only `GET BADI` on a *single-use* BAdI without implementation and without fallback raises `CX_BADI_NOT_IMPLEMENTED`.
- The BAdI interface must include `IF_BADI_INTERFACE`; the reference variable is typed with the **BAdI definition name** (`TYPE REF TO zbadi_order_check`), not with the interface.
- The execution order of multiple implementations is not something to rely on unless the BAdI supports explicit sorting of implementations.
- Classic BAdIs (SE18 "classic", `CL_EXITHANDLER=>GET_INSTANCE`) still exist in older SAP code and are migrated by SAP to new BAdIs over time; for new work always use enhancement-spot BAdIs.
- In ABAP Cloud / S/4HANA Cloud you can only implement BAdIs that SAP has *released* for key-user or developer extensibility (often via the "Custom Logic" Fiori app).

## ONE-LINE TAKEAWAY

A BAdI is an official, typed socket in someone else's code: the provider writes `GET BADI` + `CALL BADI` against an interface in an enhancement spot, and customers plug in their own classes (filtered, single- or multiple-use, with a fallback) instead of modifying the original program.
