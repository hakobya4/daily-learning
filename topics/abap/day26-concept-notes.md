# Day 26, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-25 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-24 see your own files; Day 25 `with
additional save` / `cleanup`.)

## THE TASK

Pick ONE concept -- suggestions: static actions, CDS parameters /
parameterised views, RAP BO test doubles (`cl_botd_...`), the RAP
generator, `%control` / `%tky` structures, `internal` actions, CDS
associations vs. compositions, or `mapping for` in the behavior definition
-- and explain it as if teaching a classmate who knows classic ABAP but
has never touched RAP.

## CONCEPT CHOSEN

Static actions (and how they differ from instance actions) in RAP behavior definitions.

## MY EXPLANATION (write this BEFORE looking anything up)

In RAP, an action is a custom operation on a business object that is not plain create, update or delete. Most actions are instance actions: they work on one or more existing instances that are identified by their key, for example `approveOrder` on a specific sales order. A static action is declared with the `static` keyword, as in `static action createFromTemplate result [1] $self;`, and it is NOT bound to any particular instance. It belongs to the entity as a whole, like a static method in a class, so the caller does not pass any keys. The framework calls the implementation with only the input parameters.

Typical uses are factory-like operations that create new instances (create a booking from a template, copy with defaults), or utilities that work on the entity type in general (for example, a mass import or a "get default values" action). In the behavior definition I write `static action createFromTemplate parameter ZA_Template_Param result [1] $self;`. In the behavior implementation class the handler method is declared with `FOR MODIFY IMPORTING keys FOR ACTION Order~createFromTemplate RESULT result`, and because there are no instance keys, `keys` only carries the `%param` values. Inside I can use EML `MODIFY ENTITIES ... CREATE` to create the new instance, so the new key is returned in the result.

Classic ABAP comparison: an instance action is like an instance method of an object that already exists; a static action is like a static (class) method or a factory method. Static actions have no instance based authorization or feature control (`features : instance` cannot apply to them), but they can use `features : global` and `authorization : global`. In OData they are exposed as unbound actions on the entity set instead of actions bound to a single entity.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Things to verify against the documentation: (1) static actions are bound to the entity but not to an instance, which is why the OData service shows them as bound to the collection; (2) the handler receives no instance keys, only `%cid` and `%param`; (3) with draft, a static action cannot be called on a draft instance, and the usual pattern to create drafts from a template is a static factory action; (4) a static action can also have a result of type `$self` so it returns the created instance, and Fiori elements can show it as a button on the list report toolbar.
