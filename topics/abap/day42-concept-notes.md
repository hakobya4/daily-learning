# Day 42, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as earlier days -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: determinations vs validations (`determination ... on modify/on save`, `validation ... on save`), RAP actions and functions (`action`, `static action`, factory actions, `result [1] $self`), unmanaged vs managed save (`with unmanaged save`, additional save), or authorization (`authorization : instance` / `global`, `get_instance_authorizations`) -- and explain it as if teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Determinations vs validations in a managed RAP business object.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you would put "fill this field" and "check this field" logic into the same PAI module or BAdI and hope it ran at the right moment. RAP splits them into two clearly named things in the behavior definition.

A validation checks data and can only say "ok" or "not ok". It never changes the BO. You declare it like `validation validateCustomer on save { create; field CustomerId; }`. The framework calls the implementation method at the save phase (the "check before save" step) whenever a listed trigger happened, for example the instance was created or `CustomerId` changed. If the check fails you add the key to `failed-<entity>` and a message to `reported-<entity>`, and the whole transaction is rejected, nothing is written to the database. Because it is `on save` it only runs once, at the end, so users can type half-finished data and only get the complaint when they save. (Draft: you can also bind it to the `prepare` step so drafts are checked before activation.)

A determination computes or changes data. `determination setStatus on modify { create; }` runs right after the triggering change inside the interaction phase, so the new value is immediately visible in the UI, for example default a status to 'New' or derive a total when an item amount changes. `determination setNumber on save { create; }` runs at save, which is the right place for things that must not be visible early or must be unique, such as handing out a final document number. Inside it you use `MODIFY ENTITIES ... UPDATE FIELDS` to write the result back, not direct assignment.

The mental model: validation = guard (read only, can fail the save), determination = helper (writes fields, should not fail). Both declare their triggers (`create`, `update`, or `field X`) so the framework only calls them when relevant and avoids loops; a determination that changes its own trigger field can retrigger itself, so you list only the fields it does not write.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Checks to make: (1) `on modify` determinations run during the interaction phase, which is why they can feed side effects and fresh UI values, but their changes are lost if the user discards; `on save` ones run only in the save sequence. (2) Validations cannot modify the BO, they can only fill `failed` and `reported`. (3) For draft BOs validations on `save` also run at draft activation, and `prepare` is the explicit step for pre-checks. (4) Trigger conditions matter for performance: without them the logic would run on every change.
