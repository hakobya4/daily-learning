# Day 48, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP `determination` vs `validation` (what each is for, triggers `on modify` vs `on save`, `{ create; field X; }` trigger conditions, why validations must not change data and report via `failed`/`reported`), or draft handling (`with draft`, draft actions Edit/Activate/Discard/Resume, `draft table`), or the RAP transactional phases (interaction phase vs save phase, `adjust_numbers`, `save`) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

RAP determination vs validation.

## MY EXPLANATION (write this BEFORE looking anything up)

In a classic report or BAPI you would put "fill in defaults" and "check the data" logic in the same function module. RAP splits these into two kinds of behavior-implementation hooks on a business object, declared in the behavior definition (BDEF).

A determination computes or changes data automatically when something happens to the entity. Example: `determination setStatus on modify { create; }` sets a default status when an instance is created, and `determination calcTotal on modify { field Quantity, Price; }` recalculates a total when those fields change. The trigger condition (`create`, `update`, `delete`, or `field X`) says what fires it. `on modify` runs right after the change in the interaction phase, so the UI sees the new values immediately. `on save` runs during the save phase, just before persisting, which suits things like assigning final values.

A validation only checks the state of the data and never changes it. Example: `validation checkDates on save { create; field BeginDate, EndDate; }` rejects a booking whose end date is before the begin date. Validations run `on save`, so a draft can hold incomplete data and the check only matters when the user activates or saves. If the check fails, the code does not raise an exception. It fills the `failed` table (marks the instance as failed, which stops the save) and the `reported` table (the message shown to the user).

Rule of thumb: determination = derive and set data, validation = check and reject, and validations must be side-effect free.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Both are implemented as methods in the local handler class of the behavior pool, and the framework only calls them for the instances touched by the trigger, so they receive a list of keys (`keys`) and I must read the data with `READ ENTITIES` first.
- Determinations change data through `MODIFY ENTITIES ... UPDATE`, never through direct SQL.
- Validation messages go into `reported`, and failing instances into `failed`, so that the save is rejected as a whole and nothing is half-written.
- With draft handling, determinations `on modify` also run for draft instances, while `on save` validations are not enforced until the draft is activated (unless the BDEF defines a `draft determine action Prepare`, which triggers them earlier).
