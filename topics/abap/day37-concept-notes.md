# Day 37, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-36 -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: determinations on save vs on modify,
validations and `failed`/`reported` structures, side effects
(`side effects { ... }` in the BDEF), draft `Prepare` / `Activate`,
numbering (`numbering : managed` vs early/late), or `late numbering` --
and explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

Validations in RAP and the `failed` / `reported` structures.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you would check input in a PAI module or in a BAPI and raise a message. In RAP, a validation is a method of the behavior implementation class, declared in the behavior definition, for example `validation validateCustomer on save { create; field Customer; }`. It runs during the save sequence (the "check before save" phase) and only looks at data, it never changes it. That is the difference from a determination, which computes or fills fields.

A validation receives the keys of the instances that triggered it. It reads those instances with `READ ENTITIES ... IN LOCAL MODE`, checks the values, and when something is wrong it reports back through two structures. `failed` says WHICH instance is bad (the key goes into `failed-<entity>`). That makes the framework reject the whole transaction, so nothing is saved. `reported` carries the message for the user: it holds the message object (`new_message_with_text` or a T100 message), the severity and optionally which field to highlight with `%element-<field> = if_abap_behv=>mk-on`. A message in `reported` alone does not stop the save, `failed` does.

Because validations run on save, the Fiori UI shows the errors after the user presses Save (or after Prepare in a draft scenario). Use `on modify` instead of `on save` only when you want to check immediately, but the common pattern is on save.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- `failed` and `reported` are separate on purpose: `failed` controls the outcome, `reported` controls what the user sees.
- Validations must not modify data; changing data belongs in determinations.
- Always set `%tky` (the transactional key) in both structures so draft and active instances are matched correctly.
