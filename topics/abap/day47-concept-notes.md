# Day 47, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP `action` vs `function` (state-changing vs read-only, `result`, instance vs static), `side effects` (`side effects { field X affects field Y; }`), `feature control` (instance vs global, `features : instance`), or `authorization` (`authorization master (instance)` and `DCL` access control) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

RAP `action` vs `function`

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you would write a function module or BAPI for "do something to this document", and nothing in the signature says whether it changes data or only reads. RAP makes that explicit in the behavior definition (BDEF).

An `action` is a custom operation that may change state: approve an order, cancel a booking, copy a travel. It is declared like `action approve result [1] $self;` and implemented in the behavior class (`MODIFY ENTITIES ... UPDATE`). Because it modifies data it runs inside the RAP transaction and its changes are saved with the normal save sequence (it is a modify operation, so it is subject to the same buffering and commit as create/update/delete).

A `function` is a custom operation that must not change any persistent data: it only computes and returns something, e.g. `function getDiscount result [1] ManagerDiscount;`. It is implemented with `READ ENTITIES`-style logic in the `FOR READ` handler and has no side effects on the buffer, so the framework can call it freely (it is exposed as a GET in OData while an action is a POST).

Both can be instance-bound (act on selected keys of an entity instance, the default) or static (`static action ...`, no instance needed, like a factory or a global lookup). Both can declare an input parameter (`parameter ZD_param`) and a `result` (a `[1]` or `[0..*]` structure/entity, or `$self`). Actions can additionally be enabled/disabled per instance via `features : instance`, and need authorization via `authorization : ...`.

Think of an action as a BAPI with write semantics (like BAPI_..._CREATE or _RELEASE, followed by BAPI_TRANSACTION_COMMIT) and a function as a read-only BAPI (like BAPI_..._GETDETAIL).

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- The key rule to remember: a function must not modify data; the framework relies on it, so putting a MODIFY inside a function handler is a design error, not a compile-time guarantee.
- Actions can return `$self`, which lets a Fiori UI refresh the changed instance without an extra read.
- Factory actions (`factory action copyTravel [1]`) create new instances and are a separate flavor from plain actions.
- Precise handler detail (method names such as `FOR MODIFY` vs `FOR READ` and the exact signatures) is worth re-checking against the current ABAP RAP documentation rather than relying on my memory.
