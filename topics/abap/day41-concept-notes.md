# Day 41, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as earlier days -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: draft handling (`draft table`, `Edit`/`Activate`/`Discard` actions, `with draft`), RAP side effects (`side effects { field ... affects field ... }`), numbering (`early` vs `late` numbering, `numbering : managed`), or feature control (`features : instance` vs `global`) -- and explain it as if teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Draft handling in RAP (`with draft`, the draft table and the draft actions)

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP, a half-finished entry lives in the dynpro session: if the user closes the browser or the session times out, the data is gone, or you build your own "save as incomplete" logic. RAP draft handling gives this to you as a framework feature. You add `with draft;` to the behavior definition and name a draft table (`draft table zdtravel_d`). The draft table has the same fields as the active table plus administrative fields (draft indicator, etc.). While the user edits, changes go to the draft table, not to the real table, and no business validations have to pass yet, so incomplete data can be kept for days.

The framework adds actions: `Edit` creates a draft copy of an active instance; `Activate` checks and copies the draft into the active table (and deletes the draft); `Discard` throws the draft away; `Resume` lets the user continue a draft later; `Prepare` (declared via `draft determine action Prepare`) runs the validations and determinations so errors show before activation. Since a draft of an instance exists, the active one is locked for others via a draft lock (`lock master ... `), so two people cannot edit it at once. The UI (Fiori elements) uses these automatically: the "Save" button calls Activate.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- The draft table is generated from the CDS entity (quick fix in ADT), not hand-built; it adds fields like `%is_draft` / `draftadministrativedata` handled by the framework.
- `Activate` always runs validations/determinations marked `on save` first (through Prepare); a failing validation blocks activation but not saving the draft.
- With draft, `etag master` and `lock master total etag` matter more because of long-lived edit sessions.
- Drafts are per user and persistent, so you also need to think about cleanup of stale drafts (draft administrative data keeps timestamps).
