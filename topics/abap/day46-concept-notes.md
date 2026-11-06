# Day 46, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP `determination` vs `validation` (triggers `on modify` / `on save`, what each may do), the `draft` handling (`draft table`, `Edit`/`Activate`/`Discard`), `late numbering` vs `early numbering`, or `unmanaged` vs `managed` implementation -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

RAP determination vs validation

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you would put "fill this field" and "check this input" logic into the same PAI module or BAPI. RAP splits them into two kinds of business-object logic, both declared in the behavior definition and implemented in the behavior pool.

A determination computes or changes data. Example: set a status to 'New' on create, or calculate a total from the items. It is declared like `determination setStatus on modify { create; }` or `on save { create; }`. It may change fields of the BO (via `MODIFY ENTITIES ... UPDATE`) and read other data. `on modify` runs right after the change in the transaction buffer, so the UI sees the result immediately. `on save` runs during the save sequence, for things that should happen once at the end (e.g. getting a number from a number range).

A validation only checks consistency and must never change data. It is declared like `validation checkDates on save { create; update; field BeginDate, EndDate; }`. If the data is invalid it fills the `failed` and `reported` structures (with a message pointing at the field), which makes the save fail and shows the message on the UI. Validations always run `on save`, and only when the listed triggers (create, update, fields) were actually touched.

Rule of thumb: determination = "make it right", validation = "say it is wrong". Order within the save: determinations (on modify) -> validations -> determinations on save -> persist. With draft, validations also run on Activate (the `draft determine action Prepare`).

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Validations are `on save` only (no `on modify`), and they cannot change data; they report via `failed`/`reported`.
- Determinations can be triggered by fields (`field X`) as well as by create/update/delete, so they only run when relevant data changes.
- A determination `on modify` can cause loops if it changes the very field that triggers it, so the trigger must be specific.
- Validations should be tied to the right UI fields via `%element` and `%state_area` so messages disappear once the data is corrected.
