# Day 52, Task 9 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP late numbering (`late numbering` in the behavior definition, `%pid` preliminary keys and the `adjust_numbers` saver method), RAP business events (`event` in the behavior definition, `RAISE ENTITY EVENT` in the saver, and who consumes them), or authorization control (`authorization master ( global, instance )`, `get_global_authorizations` / `get_instance_authorizations`, and `AUTHORITY-CHECK` inside them) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

Authorization control in the RAP behavior definition: `authorization master ( global, instance )`, the `get_global_authorizations` / `get_instance_authorizations` handler methods, and `AUTHORITY-CHECK` inside them (as opposed to CDS DCL roles, which I covered on day 10 / day 19).

## MY EXPLANATION (write this BEFORE looking anything up)

In a classic report or BAPI you put `AUTHORITY-CHECK OBJECT ...` wherever you felt like it -- at START-OF-SELECTION, before an UPDATE, inside the BAPI. Nothing forces you to, and every caller path has to remember it. RAP moves this into a fixed place: in the behavior definition you declare that the entity is authorization-controlled and the framework then *always* calls your check before it executes an operation, whether the request comes from Fiori, OData or EML from another ABAP program.

```
managed implementation in class zbp_i_travel unique;
strict ( 2 );

define behavior for ZI_Travel alias Travel
persistent table ztravel
lock master
authorization master ( global, instance )
{
  create;
  update;
  delete;
  action acceptTravel result [1] $self;
  association _Booking { create; }
}

define behavior for ZI_Booking alias Booking
authorization dependent by _Travel
{ update; delete; }
```

`global` = checks that do not depend on a specific record ("is this user allowed to create travels at all?"). The framework calls `get_global_authorizations` once, and it can be used to hide/disable the Create button in Fiori before anything is entered. `instance` = checks that depend on the data of one record ("may this user change THIS travel, which belongs to agency 070001?"). The framework calls `get_instance_authorizations` with the keys of the instances that are about to be updated, deleted or have an action executed. Create is only checked globally (there is no instance yet).

In the handler class:

```abap
METHOD get_global_authorizations.
  IF requested_authorizations-%create = if_abap_behv=>mk-on.
    AUTHORITY-CHECK OBJECT 'ZTRAVEL' ID 'ACTVT' FIELD '01'.
    result-%create = COND #( WHEN sy-subrc = 0 THEN if_abap_behv=>auth-allowed
                                               ELSE if_abap_behv=>auth-unauthorized ).
  ENDIF.
ENDMETHOD.

METHOD get_instance_authorizations.
  READ ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel FIELDS ( AgencyID ) WITH CORRESPONDING #( keys )
    RESULT DATA(travels).
  LOOP AT travels INTO DATA(travel).
    AUTHORITY-CHECK OBJECT 'ZTRAVEL' ID 'ZAGENCY' FIELD travel-AgencyID ID 'ACTVT' FIELD '02'.
    DATA(auth) = COND #( WHEN sy-subrc = 0 THEN if_abap_behv=>auth-allowed
                                           ELSE if_abap_behv=>auth-unauthorized ).
    APPEND VALUE #( %tky = travel-%tky
                    %update = auth  %delete = auth  %action-acceptTravel = auth ) TO result.
  ENDLOOP.
ENDMETHOD.
```

You only answer allowed/unauthorized per operation in `result`; if something is unauthorized the framework rejects the operation and you can add a message into `reported` (and `failed`) so the user sees why. Child entities usually say `authorization dependent by _Travel`, meaning "ask the parent": updating a booking is checked with the travel's instance authorization, so you write the logic once at the root.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Things I had slightly wrong: (1) The `IN LOCAL MODE` on the READ inside the handler is important -- it skips authorization and feature checks for this internal read, otherwise you'd recurse into your own check. Conversely, EML from *outside* the BO is checked, and you can only bypass it deliberately with `IN LOCAL MODE` from within the BO's own implementation (or `PRIVILEGED` with an explicit `with privileged mode` contract). (2) Authorization control in the BDEF is about *operations* (create/update/delete/actions); it does NOT filter which rows a user can read -- that is still CDS access control (DCL `define role` with `pfcg_auth`), so a real app usually needs both. (3) There is also `authorization master ( global )` alone or `( instance )` alone, and newer releases add `authorization context` for declaring which auth objects the BO checks -- I had never heard of authorization contexts. (4) Single operations can be tuned: `action acceptTravel authorization : update;` reuses the update result for that action instead of a separate check, and `authorization : none` excludes an operation (e.g. an internal action) from the check entirely, which is cleaner than returning `allowed` everywhere.
