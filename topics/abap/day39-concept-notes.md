# Day 39, Task 10 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-38 -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: early numbering vs late numbering
(`numbering : managed` vs `late numbering`), the draft handling
(`with draft`, `draft action Edit/Activate/Discard/Resume`,
`draft determine action Prepare`), side effects (`side effects`), or
ETags (`etag master LastChangedAt`) -- and explain it as if teaching
a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

ETags in RAP (`etag master LastChangedAt`) for optimistic locking

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you protect a record with a lock object (ENQUEUE/DEQUEUE), which is a pessimistic lock held on the application server. That does not work well for stateless web/OData apps: the user opens a record, goes to lunch, and meanwhile you cannot hold a lock across HTTP requests. RAP uses optimistic locking with an ETag instead. The business object has a field that changes on every update, normally a timestamp such as `LastChangedAt` (or a counter). In the behavior definition you declare `etag master LastChangedAt` on the root (and `etag dependent by _Parent` on children, which use the master's ETag). When the client reads the entity, the service returns the ETag value with it. When the client later sends an update or action, it sends that value back in the `If-Match` header. The framework compares it with the current value in the database. If they match, nobody changed the record in the meantime and the change goes through (the field is updated by the managed framework, e.g. via `@Semantics.systemDateTime.localInstanceLastChangedAt: true`). If they differ, the request is rejected with 412 Precondition Failed, and the user must reload and decide again. So: no lock is held, conflicts are detected at write time, and it fits stateless protocols.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- The ETag field must be a real field of the entity that changes on every modification; for draft-enabled BOs the total ETag is on the root, and the child entities declare `etag dependent by` the association to the parent.
- With the managed implementation, `LocalLastChanged` vs `LastChangedAt`: `LastChangedAt` is the total ETag (updated when any part of the BO tree changes), `LocalLastChanged` only tracks the entity itself.
- ETags guard against lost updates between the read and the write; they do not replace authorization or short-lived exclusive locks. With drafts, an exclusive draft lock (`lock master`) is used on top, so the two are complementary.
