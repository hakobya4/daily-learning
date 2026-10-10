# Day 19, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-18 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections.)

## THE TASK

Pick ONE concept -- suggestions: the RAP BO test double framework,
CDS associations vs. compositions, RAP business events, the additional
save / unmanaged save in a managed BO, or CDS access control (DCL) --
and explain it as if teaching a classmate who knows classic ABAP but has
never touched RAP.

## CONCEPT CHOSEN

CDS access control (DCL): `DEFINE ROLE` and `PFCG_AUTH` conditions.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you protect data with `AUTHORITY-CHECK OBJECT ...` statements that you must remember to write in every report and function module. CDS access control moves that check into the data model itself. A DCL (data control language) source holds `@MappingRole: true define role Z_I_Travel { grant select on Z_I_Travel where (CarrierId) = aspect pfcg_auth(Z_CARRIER, CARRID, ACTVT = '03'); }`. The ABAP runtime then adds the matching WHERE condition to every SELECT on that CDS view entity for the current user, based on the authorizations the user already has through PFCG roles.

So a user who may only see carrier "LH" gets only LH rows, whether the data is read by an ABAP report, an OData service, or EML `READ ENTITIES`. Nobody can forget the check, because it is part of the view's definition. Besides `pfcg_auth` you can use `aspect user`, literal conditions, and inherit conditions from another role (`inherit Z_I_Other for grant select on ...`), and define `grant select on ... where true` for unrestricted access.

In RAP it complements the behavior-side authorization control from Day 10: DCL controls which instances a user can READ (row-level, in the query), while `authorization master` / `authorization:update` in the behavior definition controls which operations or instances a user may change or trigger.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- A CDS view entity with `@AccessControl.authorizationCheck: #CHECK` and no DCL role returns no data for normal users, not everything. `#NOT_REQUIRED` switches the check off, and `#NOT_ALLOWED` forbids a role.
- The check is applied to the entity it is defined for, so projection views usually need their own role or `inherit` from the base view's role; otherwise the service sees nothing.
- DCL only filters reads. Changing data (create, update, delete, actions) is protected through the behavior definition's authorization handling, as on Day 10.
- The authorization object must exist and be maintained in the user's PFCG role; the DCL role does not grant anything, it only restricts what the user already holds.
