# Day 7, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-6, Task 9 -- pick a concept you have NOT
already written up. Day 3's pick was determinations vs. validations;
Day 4's was CDS view annotations for OData exposure; Day 5's was draft
handling; Day 6's was unmanaged vs. managed business objects; Day 2's
pick is still TODO in `day2-concept-notes.md`, so check that file too
before choosing, to avoid picking the same one twice.)

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project that you have NOT already written up -- for
example: early vs. late numbering for key generation, authorization
checks in a behavior definition (DCL -- Data Control Language),
OData V2 vs. V4 service exposure, optimistic concurrency / ETag
handling, or the difference between an action and a function in a
behavior definition -- and explain it below in your own words, as if
teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Optimistic concurrency control via ETags in RAP (the `etag master`
annotation on a behavior definition).

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP, if two users open the same record and both try to
save changes, whoever saves last just silently overwrites the other
person's work -- there's no built-in check that the record hasn't
changed underneath you since you read it. RAP's answer to that is
optimistic concurrency control, and it's called "optimistic" because
it doesn't lock the record while you're looking at it (that would be
*pessimistic* locking, which doesn't scale well for something like a
Fiori app where a user might leave a screen open for an hour). Instead,
RAP lets everyone read freely, and only checks for a conflict at the
moment you actually try to save.

The mechanism for that check is the ETag. When you mark a field in
your behavior definition with `etag master` (usually something like a
`LastChangedAt` timestamp field, though a version-number field works
too), RAP hands that field's current value back to the client
whenever it reads the entity. When the client later sends an update,
it sends that same ETag value back along with the change. RAP then
compares the ETag the client sent against the entity's CURRENT value
in the database right before applying the update. If they match,
nothing else touched the record in between, so the save goes through
normally. If they don't match, someone else already changed (and
re-saved) that record since you read it, and RAP rejects your update
with a "record has been changed" conflict instead of silently
clobbering the other person's edit. The user then has to re-read the
current data and decide how to reconcile their change, rather than
blindly overwriting.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

My mental model above was basically right on the mechanism, but I had
a couple of details fuzzy:

- I wasn't sure whether the ETag field HAS to be a timestamp. It
  doesn't -- any field that reliably changes on every update works
  (a monotonically increasing version/counter field is just as valid
  as a `LastChangedAt` timestamp; SAP's own examples lean on
  timestamps mostly because most tables already have one for audit
  purposes, not because timestamps are special to the mechanism).
- I'd assumed the ETag comparison happens somewhere deep in the
  database layer, but it's actually enforced by the RAP runtime
  framework itself, before your update/save handler method even runs
  -- so as an app developer you don't have to write the comparison
  logic by hand; you only have to declare which field is the ETag
  field, and the framework does the read-compare-reject dance for
  you at the framework layer.
- I also hadn't fully appreciated that the ETag round-trips through
  the OData protocol layer as an actual HTTP `ETag` header (and
  `If-Match` on the write request) -- it's not a RAP-internal-only
  concept, it's RAP's implementation of a standard HTTP/OData
  conflict-detection mechanism, which is presumably why it's called
  an "ETag" (entity tag) in the first place rather than some
  SAP-specific term.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

My portfolio project's managed BO already has a `LastChangedAt`
field on its root entity (added mostly for audit/traceability), so
the natural next step is to annotate it `etag master` in the
behavior definition -- that turns a field I already had for free
into real conflict protection for whenever the Fiori Elements UI on
top of it gets used by more than one person at a time, without me
having to write any manual "check before save" logic myself.
