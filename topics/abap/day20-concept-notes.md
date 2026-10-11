# Day 20, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-19 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control.)

## THE TASK

Pick ONE concept -- suggestions: the RAP BO test double framework,
CDS associations vs. compositions, RAP business events, the additional
save / unmanaged save in a managed BO, or CDS table functions -- and
explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

RAP business events (raising and consuming events from a RAP business object)

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP, when something happened in one component and others needed to react, you either called them directly or used BAdIs and class events that only work inside one system and one session. A RAP business event is the cleaner, decoupled version: a business object announces "something business-relevant happened" (for example, a sales order was created) and anybody interested can react, even in another system, without the BO knowing who they are.

In the behavior definition you declare the event, e.g. `event OrderCreated;` (optionally with a parameter such as `event OrderCreated parameter ZD_OrderCreatedParam;`). In the behavior implementation, inside the saver (the `save` / `save_modified` phase, after the point of no return), you raise it with EML-style syntax: `RAISE ENTITY EVENT zi_order~OrderCreated FROM VALUE #( ( %key = ... ) )`. The event is only really published if the transaction commits, so consumers never hear about something that was rolled back.

Consumption: in the same system a class can be an event handler (`FOR EVENTS OF zi_order`) in a local handler class of type `cl_abap_behavior_event_handler`; for other systems the event is mapped to an event binding and published via SAP Event Mesh / the enterprise event enablement, with the payload defined by the event's entity key and parameters.

Mental model: it is a "fire and forget" notification after save, versus a determination or side effect, which run synchronously inside the same transaction.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Things to double-check against the documentation: events are raised in the `save` phase of the interaction phase / saver class and are only sent after a successful commit; the event carries only the keys plus an optional parameter, not the full entity, so a consumer reads the details back with EML if it needs them. Local consumption uses a handler class with `FOR EVENTS OF`, whereas remote consumption needs an event binding in the service/event layer. Remember: events are asynchronous and decoupled, so unlike a determination they cannot block or fail the original save.
