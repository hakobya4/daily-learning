# Day 23, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-22 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-22 see your own files.)

## THE TASK

Pick ONE concept -- suggestions: factory actions, static actions,
`with additional save`, CDS parameters / parameterised views, RAP BO test
doubles, the RAP generator, `cleanup` / `cleanup finalize` in the save
sequence, or `%control` / `%tky` structures -- and explain it as if
teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Factory actions in RAP (and how they differ from static actions).

## MY EXPLANATION (write this BEFORE looking anything up)

A normal action in a RAP business object is performed on an instance that already exists, for example `approve` on a booking. A factory action is an action whose job is to CREATE new instances. It is declared in the behavior definition as `factory action copyTravel [1] parameter ... result [1] $self` or with the `[0..1]` / `[1]` cardinality, and it is implemented in the handler method of the behavior pool (`FOR MODIFY ... FOR ACTION Travel~copyTravel`). The typical example is "create a copy of this travel", where the user selects an existing row, presses a button, and a new instance is created that is pre-filled from the selected one. Inside the implementation I read the source instance with EML `READ ENTITIES`, build the new data, and use `MODIFY ENTITIES ... CREATE` to create the new instance, then fill the `mapped` structure so the framework knows the keys of the new instances (with `%cid` linking my content id to the key).

The point is that the logic of "how do I create one of these from another one" lives in the business object, not in the UI. It is available to Fiori elements and to any EML consumer. Instance-bound factory actions need a source instance (they can be `static` too, in which case they do not need one and are called on the entity as a whole, for example to create a new object with defaults). A plain static action is not about creating: it is just an action that does not need an instance key, like a utility operation on the entity. For a classic ABAP person it is like a method that works as a constructor/factory method (`create_from( ... )`) instead of an instance method like `approve( )`.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

I first thought a factory action always has to be static. Instance-bound and static factory actions both exist: instance-bound ones copy from a selected instance, static ones create from nothing (defaults or input parameters). I also had to remember that the new instance is not committed immediately: the action only creates it in the transactional buffer and returns it in `mapped`, and the normal save sequence persists it, so determinations and validations on create still run for the copy. For drafts, the new instance is created as a draft. A factory action cannot be used to change or delete existing instances, that is what ordinary actions and update/delete operations are for.
