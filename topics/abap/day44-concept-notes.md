# Day 44, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as earlier days -- pick a concept you have NOT already written
up. Check the earlier day files in this folder for what is covered.)

## THE TASK

Pick ONE concept -- suggestions: RAP optimistic locking (`lock master`, `etag master LastChangedAt`, `etag dependent by`), the difference between `managed` and `unmanaged` implementation types, `determination` vs `validation` trigger times (`on modify` / `on save`), or `draft` handling (`with draft`, `draft action Edit/Activate/Discard/Resume`) -- and explain it as if teaching a classmate who knows classic ABAP enqueue locks and `UPDATE` statements but has never touched RAP.

## CONCEPT CHOSEN

RAP optimistic locking (`lock master`, `etag master`, `etag dependent by`).

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you call an enqueue function module to set a lock-table entry before editing, which blocks other users for the whole editing time (pessimistic locking). That does not suit stateless OData/Fiori apps, where each request is a separate session.

RAP uses optimistic locking instead. The business object declares an ETag field, typically `LastChangedAt`, with `etag master LastChangedAt` in the behavior definition. When the UI reads an instance it receives the ETag value; when it sends a modify, it sends the value back via the If-Match header. At save time the framework compares it with the value in the database. If someone changed the record in between, the values differ and the request fails (HTTP 412 Precondition Failed), so nobody's change is silently overwritten.

`lock master` marks the root entity as the one that takes a short-lived exclusive lock during the actual modify/save phase (in managed RAP, generated from the lock object); child entities declare `lock dependent by _Parent`. For child entities that have no own ETag field, `etag dependent by _Parent` means the root's ETag is used. So users can read and edit simultaneously without blocking each other, and conflicts are detected when saving instead of prevented up front.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Pessimistic locking (enqueue) is still used briefly in RAP (`lock master`), but only around the save, not for the whole UI editing session; with draft, the long-lived lock is the draft lock.
- The ETag field must be updated on every change (e.g. a `@Semantics.systemDateTime.localInstanceLastChangedAt` field that managed RAP maintains automatically).
- `etag master` is on the root; children use `etag dependent by`.
