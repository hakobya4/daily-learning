# Day 33, Task 9 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-32 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 26 static actions; Day 27 CDS associations vs.
compositions; Day 32 see its file; other days: see your own files.)

## THE TASK

Pick ONE concept -- suggestions: the RAP `%cid` / `%cid_ref` mechanism for
chaining creates in one EML call, `READ ENTITIES ... FIELDS` vs.
`ALL FIELDS WITH`, `FAILED` / `REPORTED` / `MAPPED` response structures,
`ABAP SQL` aggregate expressions and `GROUP BY`, inline declarations and
constructor expressions (`VALUE`, `CORRESPONDING`, `COND`, `REDUCE`),
`CDS custom entities`, or the clean-core / released-API idea -- and
explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

The RAP `%cid` / `%cid_ref` mechanism for chaining creates in one EML call.

## MY EXPLANATION (write this BEFORE looking anything up)

When you create a new instance with EML (`MODIFY ENTITIES OF ... CREATE`), the real key does not exist yet: with managed late numbering it is only assigned during the save sequence. So how do you refer to the new instance in the same call, for example to create a child item under a header you are creating right now? `%cid` is the answer. It is a "content ID", a temporary label you choose yourself (a string like `'H1'`) that is only valid inside that one MODIFY call. You put it in the CREATE entry for the header (`%cid = 'H1'`), and in the child's `CREATE BY \_Items` you refer to the parent with `%cid_ref = 'H1'`. RAP resolves it internally.

Afterwards the `MAPPED` response table tells you which `%cid` ended up as which real key (`%tky`), and `FAILED` / `REPORTED` use the same identification, so you can tell which of your entries went wrong. Think of it like a local variable name for an object that has no primary key yet, similar to a temporary document number in classic ABAP before the number range is drawn. Each `%cid` must be unique within the call. `%cid_ref` can also refer to an instance created earlier in the same call by an action or another create.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- The `%cid` only lives for the duration of the single EML statement (or the same chained batch); it is not a key and must not be stored.
- The real key is only final after the save sequence with late numbering; the key in `MAPPED` after the MODIFY may still be a temporary (`%pid`-based) one, so read the final key after COMMIT ENTITIES using the mapped result.
- A `%cid` must be unique per call, and for a create-by-association the parent is identified either by its real key (existing instance) or by `%cid_ref` (instance created in the same call), not both.
