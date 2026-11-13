# Day 53, Task 9 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP side effects (`side effects { field ... affects field ...; action ... affects ... }` in the behavior definition and why a Fiori Elements UI needs them to refresh the right fields), unmanaged save in a managed BO (`with unmanaged save` and the `save_modified` saver method calling a legacy function module or BAPI), or CDS virtual elements (`@ObjectModel.virtualElementCalculatedBy`, the `IF_SADL_EXIT_CALC_ELEMENT_READ` class, and why the value is not available in a plain `SELECT`) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

`precheck` in RAP behavior definitions -- rejecting a create/update/delete/action request
before it ever reaches the transactional buffer. (The three suggested topics are already covered:
side effects on day 11/43, unmanaged save on day 21, virtual elements on day 16/36.)

## MY EXPLANATION (write this BEFORE looking anything up)

In a classic BAPI you usually do two things in one go: check the input, and if it's fine, write
it (or put it in an update task). In RAP these are split into phases. When a request comes in --
say the Fiori app sends an update for a travel's `BeginDate` -- the framework applies it to the
**transactional buffer** first, and validations only run much later, in the save sequence (or
when a draft is activated). So by the time a validation complains, the bad value is already
sitting in the buffer (or the draft table) and the user has been allowed to type around it.

`precheck` is a hook that runs **before** the modification is applied to the buffer. You declare
it on the operation in the behavior definition:

```
define behavior for ZI_Travel alias Travel
...
{
  create ( precheck );
  update ( precheck );
  delete ( precheck );
  action ( precheck ) acceptTravel result [1] $self;
}
```

and the framework then requires a handler method in the behavior pool, e.g.

```abap
METHODS precheck_update FOR PRECHECK
  IMPORTING entities FOR UPDATE Travel.
```

Inside it you get the **incoming** values (the `entities` table, with `%control` telling you
which fields were actually sent), you check them -- e.g. "the agency ID must exist", "this
customer is blocked", "you may not change the currency once the travel is accepted" -- and for
every rejected instance you fill `failed-travel` (with the `%tky`) and `reported-travel` (with a
message and `%element` so the UI can highlight the field). Rejected instances are simply never
written to the buffer; the rest of the request goes through. Because it runs so early, the
precheck typically only sees the request data, so if you need the current state you READ
ENTITIES yourself.

Compared to a validation: a precheck is "don't even let this change in", a validation is "the
whole object, in its final state, must be consistent before it can be saved". Prechecks are good
for cheap checks on the incoming request (and especially important in **draft** scenarios,
where nothing else stops junk from being stored in the draft table between roundtrips);
validations are still needed for cross-field rules on the final state, since a precheck only
ever sees one request at a time. Feature control is different again: it hides or disables the
operation in the UI up front, whereas a precheck answers an actual request with an error.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- I first thought precheck was a managed-only feature; it is available for both managed and
  unmanaged BOs, and the method signature is the same (`FOR PRECHECK ... FOR CREATE/UPDATE/
  DELETE/ACTION`).
- The precheck method only receives the request data, not the buffered instance, so a check like
  "is the status still open?" needs its own READ ENTITIES IN LOCAL MODE.
- Errors from a precheck must go into `failed` *and* `reported`; filling only `reported` shows a
  message but the change is still applied.
- It does **not** replace validations: an EML caller can bypass a UI flow, and a sequence of
  individually-valid updates can still leave the object inconsistent, which only a validation on
  the final state catches.
