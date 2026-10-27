# Day 36, Task 8 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-35 -- pick a concept you have NOT already written
up. See the earlier day files in this folder for what has been covered.)

## THE TASK

Pick ONE concept -- suggestions: value helps (`@Consumption.valueHelpDefinition`),
virtual elements (`@ObjectModel.virtualElement` with a calculation class),
unmanaged save (`with unmanaged save`), RAP business events, `projection`
behavior definitions and `use action`, or `CDS custom entities` -- and explain
it as if teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

Virtual elements (`@ObjectModel.virtualElement`) with an ABAP calculation class.

## MY EXPLANATION (write this BEFORE looking anything up)

A virtual element is a field on a CDS view that has no column in the database. Its value is computed in ABAP at read time instead. In classic ABAP you'd add a field to an ALV output table and fill it in a loop after the SELECT; a virtual element is the RAP equivalent, but declared on the CDS entity so every consumer (Fiori UI, OData service) gets it.

You declare it in the (projection) view with annotations: `@ObjectModel.virtualElement: true` and `@ObjectModel.virtualElementCalculatedBy: 'ABAP:ZCL_MY_CALC'`, on an element such as `cast( 0 as abap.dec(15,2) ) as DiscountedPrice`. The class implements `IF_SADL_EXIT_CALC_ELEMENT_READ` with two methods: `get_calculation_info`, where you tell the framework which real fields you need so it selects them, and `calculate`, which receives the already-read rows and fills the virtual field for each. It runs after the data is read and on the result set only, so it can't be used for filtering or sorting in the database, and it should avoid per-row SELECTs.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- Virtual elements can't be used in WHERE or ORDER BY on the database side, since the value doesn't exist there; filtering on them has to happen elsewhere or be avoided.
- `get_calculation_info` matters: if you forget to request the base fields you read in `calculate`, they come back initial.
- If the logic can be expressed in SQL (CASE, arithmetic, built-in functions), a normal CDS expression is better; use a virtual element only for logic that needs ABAP.
