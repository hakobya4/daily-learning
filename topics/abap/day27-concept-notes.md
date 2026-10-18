# Day 27, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-26 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 21-25 see your own files; Day 26 static
actions.)

## THE TASK

Pick ONE concept -- suggestions: CDS parameters / parameterised views,
RAP BO test doubles (`cl_botd_...`), the RAP generator, `%control` /
`%tky` structures, `internal` actions, CDS associations vs.
compositions, `mapping for` in the behavior definition, or CDS
extension views -- and explain it as if teaching a classmate who knows
classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

CDS associations vs. compositions

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you join tables yourself in every SELECT. In CDS you can instead declare a relationship once with an association (`association [0..1] to I_Customer as _Customer on $projection.CustomerId = _Customer.CustomerId`) and expose it in the select list as `_Customer`. The join is only executed when a consumer actually uses the path (`_Customer.Name`), so it is a lazy, reusable join, and OData can turn exposed associations into navigation properties.

A composition is a stronger kind of association: it says the target is a child that is part of the parent (`composition [0..*] of ZI_Item as _Item`). In RAP this defines the business object tree: root and child entities, with the child's lifecycle (create, delete, lock, draft) owned by the root. A plain association is only a reference to an independent entity, such as a customer. Child entities need `association to parent` back to the root.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Associations are not always lazy joins: they are resolved only when used, but exposing them does not cost anything until then. Compositions also require the parent/child behavior definitions to be consistent: the root declares `association _Item { create; }` and the child uses `lock dependent by` and `authorization dependent by` the parent. Cardinality (`[0..1]`, `[1..*]`) matters for how joins and OData navigations behave.
