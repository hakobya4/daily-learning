# Day 24, Task 8 -- ABAP/RAP: explain one concept in your own words

(Same format as Days 2-23 -- pick a concept you have NOT already written
up. Earlier picks: Day 3 determinations vs. validations; Day 4 CDS
annotations for OData; Day 5 draft handling; Day 6 unmanaged vs.
managed; Day 7 ETags; Day 8 early vs. late numbering; Day 9 actions vs.
functions; Day 10 authorization control; Day 11 side effects; Day 12
feature control; Day 13 the save sequence; Day 14 value helps; Day 15
EML; Day 16 virtual elements; Day 17 lock master / lock dependent; Day 18
projection views and behavior projections; Day 19 CDS access control;
Day 20 business events; Day 23 factory actions; Day 21-22 see your own files.)

## THE TASK

Pick ONE concept -- suggestions: `with additional save`, static actions,
CDS parameters / parameterised views, RAP BO test doubles, the RAP
generator, `cleanup` / `cleanup finalize` in the save sequence,
`%control` / `%tky` structures, or `strict ( 2 )` mode -- and explain it
as if teaching a classmate who knows classic ABAP but has never touched RAP.

## CONCEPT CHOSEN

`strict ( 2 )` mode in RAP behavior definitions

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you can usually get away with sloppy code and the compiler only warns you. A RAP behavior definition works the same way by default: it is permissive about things that are probably mistakes. Writing `strict ( 2 )` right after the implementation type (`managed implementation in class ... unique; strict ( 2 );`) switches on a stricter set of syntax checks, a bit like `use strict` in other languages or like the strict mode of Open SQL. The number is the version of the rule set; 2 is the newer one and includes everything from 1.

With strict mode the framework forces you to be explicit and consistent: for example you must declare authorization (`authorization master ( instance )` or `global`) instead of silently having none, determinations and validations must state their trigger operations and fields exactly, and the compiler complains about things like missing `lock` definitions or implicit field handling. Strict mode 2 adds further checks on top, for instance around the `%control` handling, `%tky` usage, and requirements that make the BO ready for features such as draft and for the newer EML. The point is that errors that would show up as strange runtime behavior are turned into compile-time errors.

For a classmate from classic ABAP: it is like turning on the extended program check and making warnings into errors, but built into the language for RAP. New BOs should always start with strict mode, because switching it on later means fixing every violation at once.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

I first thought strict mode only affects syntax warnings. It also guarantees that the BO follows the current RAP best practices, so it is a prerequisite for several newer features, and the higher number includes the lower ones. I also should not claim exact lists of checks from memory; the authoritative list is in the ABAP keyword documentation for `strict` in BDEF, so I should check there before relying on specific rules.
