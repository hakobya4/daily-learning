# Day 45, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP `action` vs `function` (state-changing vs read-only, `result [1] $self`), `side effects` declarations in the behavior definition, `mapping for` / field mapping in managed RAP, or `authorization master (instance)` vs `(global)` -- and explain it as if teaching a classmate who knows classic ABAP function modules and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

RAP `action` vs `function`

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you would write a function module or BAPI for every operation on a business object, and nothing in the signature told you whether it changed data. RAP makes that distinction explicit in the behavior definition, and both are declared on an entity and implemented in the behavior pool.

An **action** is a custom operation that may change state: for example `action approve result [1] $self;` on a travel entity sets a status field and saves it. Because it modifies data it takes part in the RAP transaction: it runs in the modify phase, changes are buffered, and they are persisted at the save sequence together with everything else. The `result [1] $self` part says the action returns the (changed) instance of the same entity, so a Fiori UI can refresh the row without a second read. Actions can be instance-bound or static, can have an input parameter structure (`parameter ...`), and can be exposed in the UI via annotations.

A **function** is read-only: `function getDiscountedPrice result [1] $self`-style operations compute and return something but must not change persistent data, so they are safe to call repeatedly and are mapped to HTTP GET in OData, whereas actions map to POST. That is the closest analogue to a BAPI like `..._GETDETAIL` versus `..._CHANGE`.

Side effects are a separate declaration (`side effects { field x affects field y; }`) telling the UI which other fields or entities to reload after an action or field change; they are about UI refresh, not about the logic itself.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Actions and functions both need an implementation method in the behavior pool, but only actions get `MODIFY ENTITIES ... UPDATE` in the body; a function only does `READ ENTITIES` and fills `result`.
- Functions can be marked with `result [1] $self` or return a custom abstract entity (`result [0..n] ...`); I should not assume `$self` for every function.
- The save is not triggered by the action itself; the framework persists buffered changes during the save phase, and `precheck`/`validation` logic can still reject the change.
- Authorization for an action is checked via `authorization master (instance)` / `(global)` and `%action-<name>` in the authorization methods, which is a topic of its own.
