# Day 10, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-9 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags/optimistic concurrency; Day 8 early vs. late
numbering; Day 9 actions vs. functions.)

## THE TASK

Pick ONE concept -- suggestions: authorization control with DCL
(`define role`) and `authorization master`, virtual elements in CDS,
side effects for UI refresh, value helps
(`@Consumption.valueHelpDefinition`), or the RAP save sequence
(interaction phase vs. save phase, `late numbering`, `additional save`)
-- and explain it as if teaching a classmate who knows classic ABAP but
has never touched RAP.

## CONCEPT CHOSEN

Authorization control in RAP: DCL access control (`define role`) and
`authorization master` in the behavior definition.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP I protect data by calling `AUTHORITY-CHECK OBJECT ...`
by hand wherever I read or change something, and it is easy to forget
one place. RAP splits authorization into two declarative layers. The
first is READ access: a CDS access control (`@MappingRole: true
define role ZI_Booking { grant select on ZI_Booking where (Carrier) =
aspect pfcg_auth(ZCARRIER, ZCARRIER, ACTVT = '03'); }`) which adds a
filter to the CDS view so users only ever get rows they are allowed to
see, regardless of which service or app reads the view. The second is
WRITE access: in the behavior definition I declare `authorization master
( instance )` (checks per instance, using the data of the row) or
`( global )` (checks that do not depend on a row, like "may this user
create at all"), and I implement `get_instance_authorizations` /
`get_global_authorizations` in the behavior pool. These return
`%update`, `%delete`, `%action-<name>` etc. as authorized or
unauthorized, and Fiori then disables the matching buttons. Dependent
child entities use `authorization dependent by _Parent` so I only
define it once at the root.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

- A CDS view without any access control is open to everyone unless the
  view is annotated `@AccessControl.authorizationCheck: #NOT_REQUIRED`
  explicitly; `#CHECK` means a missing role means no data is returned.
- Global vs. instance authorization are different methods; create is
  usually global because no instance exists yet.
- The authorization checks are about whether the operation is allowed;
  they do not replace validations, which check data correctness.
- `authorization master` and the DCL role protect different paths (write
  vs. read), so I need both for a complete setup.
- I should double-check exact keyword syntax in the RAP documentation
  before relying on my examples above.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

In my portfolio RAP app, a user should only see bookings of their own
region, which is a DCL role on the interface view, and only managers may
run the `cancel` action, which is instance authorization on that action
in the behavior pool. That keeps security rules declared next to the
data model instead of scattered through UI code.
