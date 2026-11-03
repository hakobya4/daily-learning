# Day 43, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as earlier days -- pick a concept you have NOT already written
up. Check the earlier day files in this folder for what is covered.)

## THE TASK

Pick ONE concept -- suggestions: RAP authorization (`authorization master ( instance )`, `authorization master ( global )`, `get_instance_authorizations`, `get_global_authorizations`, `%action-...` / `%update` result fields), side effects (`side effects { field X affects field Y; }`), `late numbering` vs early numbering, or `lock master` / `etag master` for optimistic locking -- and explain it as if teaching a classmate who knows classic ABAP `AUTHORITY-CHECK` and enqueue locks but has never touched RAP.

## CONCEPT CHOSEN

RAP side effects (`side effects { field X affects field Y; }`) -- telling the Fiori UI what to refresh after a change.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic dynpro programming, changing one field could trigger PBO/PAI logic that recalculated other fields on the screen. A Fiori elements app has no such round trip: it edits a draft and only talks to the backend when needed. So when a user changes `Quantity` and the backend determination recomputes `NetAmount`, the UI does not know the displayed `NetAmount` is stale.

Side effects are a declaration in the behavior definition that tells the UI this. Example: `side effects { field Quantity affects field NetAmount; }`. After the user changes Quantity, the UI sends a request to read the affected field(s) again and updates the screen. Other forms: `field X affects entity _Items` to reload an association, `action Confirm affects field Status`, and `determine action Prepare { ... }` which lets the UI run validations early on the draft ("determine action"), with `$self` meaning the whole instance.

The rule of thumb: determinations and validations do the actual logic on the server; side effects only say which parts of the screen to reload. They change no data themselves and are metadata that goes into the service metadata.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Side effects are not needed for fields changed by the user, which the UI already shows; they matter for fields changed by the backend (determinations, actions).
- Without the declaration the data is still correct in the database/draft; the UI simply shows the old value until the next reload, so it is a UX bug, not a data bug.
- Mistake to avoid: expecting a side effect to trigger the determination. The determination is triggered by its own `on modify { field ... }` trigger condition; the side effect only causes the refresh afterwards.
