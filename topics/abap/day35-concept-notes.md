# Day 35, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-34 -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: draft handling (`draft table`, `Edit`/`Activate`/`Discard`
actions), side effects in behavior definitions (`side effects { field X affects field Y; }`),
`determination on save` vs `on modify`, numbering (`early` vs `late` numbering, `managed`
numbering), `ETag` / optimistic locking (`etag master`), or CDS access control (DCL,
`DEFINE ROLE`, `GRANT SELECT ON ... WHERE`) -- and explain it as if teaching a
classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

ETag / optimistic locking (`etag master`) in RAP behavior definitions.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you protect against two users editing the same record with enqueue locks (SM12), which are pessimistic: the record is locked while someone edits. That does not work well for stateless OData/Fiori apps, because there is no long-lived session holding the lock. RAP uses optimistic locking with an ETag instead. You pick a field that changes on every update, usually a `last_changed_at` timestamp (`LocalLastChangedAt`), and declare it in the behavior definition with `etag master LocalLastChangedAt`. When the client reads an instance, the service returns the ETag value. When the client later sends an update or delete, it sends that value back (If-Match). The framework compares it with the current value in the database; if someone changed the record in between, the values differ and the request fails with a precondition failed error (HTTP 412) instead of silently overwriting the other user's work. With `managed` implementations and a field annotated with `@Semantics.systemDateTime.localInstanceLastChangedAt: true`, the framework fills the field automatically. For child entities you use `etag dependent by _Parent` so the root ETag guards the whole composition. The classic analogy: instead of locking the book while you read it, you note the edition number and the librarian rejects your correction if the edition has moved on.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- The ETag field must really change on every modification, otherwise conflicts go undetected; a managed timestamp field solves that.
- ETag checks are not a replacement for the `lock master` statement, which still handles short-lived locks during the save sequence; the two complement each other.
- Child entities use `etag dependent by` rather than declaring their own master ETag.
