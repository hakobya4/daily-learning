# Day 17, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-16 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements.)

## THE TASK

Pick ONE concept -- suggestions: the RAP BO test double framework,
CDS associations vs. compositions, projection views and behavior
projections, `lock master` / `lock dependent`, RAP business events, or
the additional save / unmanaged save in a managed BO -- and explain it as
if teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Lock master / lock dependent (RAP pessimistic locking).

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP, you protect a record by calling an enqueue function module (generated from a lock object) before changing it, so nobody else can edit it at the same time. In RAP the idea is the same, but it is declared in the behavior definition instead of being called by hand.

On the root entity of a business object you write `lock master`. This tells the framework that editing the root instance needs an exclusive lock, and that the lock covers the whole BO tree. In a managed BO the framework only does the locking for you if you also say how; in an unmanaged BO you implement the `lock` method in the handler class and call the enqueue yourself (for example the generated `ENQUEUE_...` function module), raising a failed/reported message if the lock is already taken by another user.

Child entities that are part of the same composition get `lock dependent by _Parent`. That says "I do not lock myself; lock my parent (the master) instead", so locking a header also protects its items, and two users cannot edit different items of the same document at once in a conflicting way. The `by` part names the association to the master.

Lock is one half of concurrency control. It prevents two users editing at the same time (pessimistic). ETags (Day 7) detect that data changed between reading and saving (optimistic). A BO often uses both: the lock keeps editors out while a change is in progress, and the ETag catches stale data if the user was looking at an old copy.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

My understanding of the idea (master/dependent, lock covers the tree) is right. Things to be careful with: `lock master` only appears on the root, and `lock dependent` only on non-root entities, never both on one entity. In a managed BO with draft, the draft table also takes an exclusive draft lock when a draft is created, so the real lock on the active instance is only taken at activation or edit. For a managed implementation without `unmanaged` you can use `lock master` alone and the framework generates the standard lock; custom lock objects are only needed when you add `unmanaged lock`. Check against the current ABAP RAP documentation for exact keywords before relying on the last point.
