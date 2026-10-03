# Day 12, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-11 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags/optimistic concurrency; Day 8 early vs. late
numbering; Day 9 actions vs. functions; Day 10 authorization control;
Day 11 side effects.)

## THE TASK

Pick ONE concept -- suggestions: virtual elements in CDS, value helps
(`@Consumption.valueHelpDefinition`), the RAP save sequence
(interaction phase vs. save phase, `additional save`, `with unmanaged
save`), the RAP BO test double framework, feature control
(`features : instance`), or CDS associations vs. compositions -- and
explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

Feature control (`features : instance`) in RAP behavior definitions.

## MY EXPLANATION (write this BEFORE looking anything up)

Feature control decides, per field, action or operation, whether the UI
lets the user use it right now. For example a booking that is already
"Accepted" should not allow the Accept action again, and the field
`TravelID` should be read-only after creation. In the behavior definition
you declare `field ( features : instance ) Status;` or
`action ( features : instance ) acceptTravel result [1] $self;`, and in the
behavior implementation class a method `get_instance_features` reads the
current instance data and fills a result structure: for each instance it
sets `%action-acceptTravel = if_abap_behv=>fc-o-enabled` or `-disabled`,
and `%field-Status = if_abap_behv=>fc-f-read_only` or `-mandatory`. Fiori
elements then greys out buttons and fields accordingly. There is also
`features : global` for things that do not depend on the instance, for
example the current user's general ability to create. In classic ABAP I
would have set screen attributes in PBO (`LOOP AT SCREEN`); here the
rules are modelled once on the backend and the UI follows them.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

- Feature control is only for the UI/enablement; it is NOT a security check. A direct OData call can still try the action, so I still need validations or authorization control on the backend to enforce the rule.
- It is different from authorization control (who may do something) because it depends on the data state (what is possible now).
- I need to check the exact names of the constants in the result structure (`if_abap_behv=>fc-o-*` for operations/actions, `fc-f-*` for fields) and how static `( mandatory )`/`( readonly )` differs from dynamic `features : instance`.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio RAP app, status-driven actions (approve, cancel, reject) should be enabled only in the right status, and key fields should become read-only after creation. I would implement that with `features : instance` and back it up with a validation.
