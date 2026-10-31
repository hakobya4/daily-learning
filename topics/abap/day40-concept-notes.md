# Day 40, Task 10 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as earlier days -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: validations vs determinations (triggers and
timing `on save` / `on modify`), unmanaged save (`with additional save`,
`cleanup`), CDS value helps (`@Consumption.valueHelpDefinition`), or
projection behavior definitions -- and explain it as if teaching a classmate
who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Validations vs determinations in RAP behavior definitions (and their triggers/timing)

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP the business rules for a transaction are scattered: checks in a dynpro PAI, field defaults in a BAdI, consistency checks in a save function module. RAP names these roles and runs them for you at defined moments.

A determination computes or derives data. Example: set the status to "New" when a travel is created, or recalculate the total price when a booking changes. It changes the instance's fields and is declared like `determination setStatus on modify { create; }` or `determination calcTotal on save { field BookingFee; }`.

A validation only checks, never changes data. If the check fails, it adds a message to `reported` and the key to `failed`, which makes the save fail. Example: `validation checkDates on save { create; field BeginDate, EndDate; }` rejects a travel whose end date is before its begin date.

Timing: `on modify` runs right after the change in the interaction phase, so the UI sees the derived value immediately (good for defaults and values the user needs to see). `on save` runs in the finalize/check-before-save phase, once, just before the commit, so it sees the final state (good for expensive checks and cross-field checks). Validations are only `on save`. The trigger list (`create`, `update`, `field X`, `delete` for validations) tells the framework when to call it, so it does not run when unrelated fields change. A validation also has a side effect on drafts: with draft, `on save` validations run on the Prepare step (`draft determine action Prepare`), so errors show before activation.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Validations belong to the `on save` phase only; I first assumed `on modify` was possible for them. Only determinations can be `on modify`.
- A determination `on save` that sets fields must not be triggered by the fields it changes, otherwise it can loop; the trigger list should contain only its inputs.
- Use `READ ENTITIES` inside the handler to get the current (including unsaved) state, then `MODIFY ENTITIES` in a determination; validations must not use MODIFY.
- Order matters: determinations run before validations in the save sequence, so a validation sees the derived values.
