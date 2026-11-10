# Day 50, Task 9 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP determinations vs validations (triggers `on modify` / `on save`, `create`/`update` triggers, when each runs), draft handling (`with draft`, draft tables, `Edit`/`Activate`/`Discard`), or RAP actions and functions (instance vs static, `result [1] $self`, factory actions) -- and explain it as if teaching a classmate who knows classic ABAP reports and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

Internal actions in RAP (`internal action` in the behavior definition) -- actions that exist in the business object but are not exposed to the outside world.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you have public BAPIs, but also private helper methods that only your own code calls. A RAP business object has the same split. A normal `action` (for example `action acceptTravel result [1] $self;`) is exposed: it shows up in the OData service and a Fiori button can call it, and it is also callable through EML from other code. If you add the keyword `internal` (`internal action recalcTotals;`), the action is part of the BO and has a proper implementation in the behavior pool, but it is not published through the service projection, so no UI or OData client can call it. Only code inside the same BO can trigger it, for example a determination or another action using `MODIFY ENTITIES ... EXECUTE recalcTotals`.

Why use it? It lets you put reusable business logic (recalculate totals, set a status, copy data) in one place with the usual RAP benefits: the action runs against the transactional buffer, gets `%tky` keys, can fill `failed` and `reported`, and respects the save sequence. Without `internal` you would either duplicate the logic in several determinations or accidentally expose a technical step to end users. The same keyword also works for other operations, such as `internal create` or `internal update`, when you want to forbid external callers from changing data but still let your own code do it.

Example: a determination `on modify { create; }` on the item entity calls the internal action `recalcTotals` on the root, so totals are updated whenever items change, but the user never sees a "Recalculate" button.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Things to keep straight: internal actions must still be listed in the behavior definition and implemented in the behavior pool like any other action; they simply are not exposed in the behavior projection (you cannot `use action` them there). They are also not subject to the instance-feature or authorization checks of the UI layer, because only the BO's own code can call them, so any needed checks must be done by the caller or inside the action. Also, "internal" does not mean "private to one entity": other entities of the same BO (and its own EML calls from the BO implementation) can use it, but consumers outside the BO cannot.
