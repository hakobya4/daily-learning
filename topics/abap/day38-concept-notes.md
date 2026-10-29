# Day 38, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-37 -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: static actions vs instance actions,
factory actions (`factory action copyX [1]`), action parameters
(`action x parameter ZA_Param`), `internal` actions/determinations,
or feature control (`features : instance`) -- and explain it as if
teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Static actions vs instance actions, and factory actions.

## MY EXPLANATION (write this BEFORE looking anything up)

An action in RAP is a custom operation on a business object that is not plain create, update or delete, for example "approve", "cancel" or "copy". It is declared in the behavior definition and implemented as a method in the behavior pool. In classic ABAP this would be a method on an object or a function module called from a button.

An instance action works on one or more existing instances, selected by their keys: `action approve result [1] $self;`. The framework passes the keys of the selected rows to the method, and I READ the data for those keys, change it with `MODIFY ENTITIES`, and return the result. Typical use: a button in the object page or list report for the selected row.

A static action (`static action createDefault`) is not tied to an instance. It receives no keys, so it is like a static class method in ABAP. It is good for things like "load defaults" or an operation across the whole entity. Because there is no instance, it cannot use instance feature control.

A factory action creates new instances: `factory action copyTravel [1]` (instance factory action, copies from the selected instance) or `static factory action createTravel [1]`. The method fills `mapped` with the new key, and the framework then handles it as a create. The result is always a new instance of the same entity, so there is no `result` clause.

Action parameters (`action x parameter ZA_Param`) let the UI ask the user for input in a dialog before the action runs. Actions can be restricted with feature control (`features : instance`), so a button is enabled or disabled per row depending on state, for example "approve" only enabled when status is open.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- A factory action must return created keys through `mapped`, not through a `result` parameter.
- Static actions can still use global feature control (`features : global`), just not per-instance control.
- Actions run inside the RAP transaction, so their changes are committed in the save sequence, not immediately.
