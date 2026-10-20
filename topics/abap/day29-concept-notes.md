# Day 29, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-28 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-25 see your own files; Day 26 static
actions; Day 27 CDS associations vs. compositions; Day 28 see your file.)

## THE TASK

Pick ONE concept -- suggestions: CDS parameters / parameterised views,
RAP BO test doubles (`cl_botd_...`), the RAP generator, `%control` /
`%tky` structures, `internal` actions, `mapping for` in the behavior
definition, CDS extension views, or `determine action`-style
determinations on save -- and explain it as if teaching a classmate who
knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

`%control` and `%tky` structures in RAP.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you pass a structure and hope the caller filled the right fields. RAP needs to know more: which instance is meant, and which fields the caller actually wants changed. That is what these special components are for.

`%tky` (transactional key) identifies one instance. For a non-draft BO it is just the semantic key, but for a draft-enabled BO it also contains `%is_draft`, so the same business key can address either the active or the draft version. That is why you write `keys = VALUE #( ( %tky = <row>-%tky ) )` in EML instead of listing bare key fields.

`%control` is a structure of flags, one per field, set to `if_abap_behv=>mk-on` or `mk-off`. In an update request it says which fields in the data part were really supplied. Without it, an initial value would be ambiguous: "set to blank" or "not provided". With `%control` the framework only changes fields flagged on, much like a PATCH instead of a PUT. In handler methods it lets you check what the user changed, for example in a determination or validation.

Mnemonic: `%tky` answers "which instance?", `%control` answers "which fields?".

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

`%tky` is a shorthand for `%key` plus `%pid` and `%is_draft` where applicable, so it is the safe default. `%control` is filled automatically by the framework for Fiori requests, but in your own EML `MODIFY` calls you must set it yourself, usually through the `%control-field = if_abap_behv=>mk-on` pattern or `FIELDS ( ... ) WITH` syntax, which generates it for you.
