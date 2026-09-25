# Day 4, Task 9 -- ABAP/RAP: explain one concept in your own words

(Same format as Day 2 and Day 3, Task 9 -- pick a concept you have NOT
already written up. Day 3's pick was determinations vs. validations;
Day 2's pick is still TODO in `day2-concept-notes.md`, so check that
file too before choosing, to avoid picking the same one twice.)

## THE TASK

Pick ONE concept you're using (or plan to use) in your ABAP/RAP
portfolio project that you have NOT already written up -- for
example: CDS view annotations (`@ObjectModel`, `@Consumption`,
`@Search`), draft handling, unmanaged vs. managed BOs, exposing an
OData service, or authorization checks in RAP -- and explain it below
in your own words, as if teaching a classmate who knows classic ABAP
but has never touched RAP.

## CONCEPT CHOSEN

CDS view annotations for OData exposure (`@ObjectModel`,
`@Consumption`, `@Search`) -- different from Day 2's pick (still
open) and Day 3's pick (determinations vs. validations).

## MY EXPLANATION (write this BEFORE looking anything up)

A CDS view on its own is just a SELECT wrapped in a reusable database
artifact -- the annotations are what tell the framework how that view
should behave once it's exposed as an OData service. `@ObjectModel`
annotations describe the view's role in the data model: whether it's
the root of a business object hierarchy, which fields are keys, and
which associations represent compositions (parent-child, cascading
delete) versus plain associations (just a reference). `@Consumption`
annotations control how a field shows up to a consumer, like a Fiori
app -- `@Consumption.valueHelpDefinition` wires up an F4 dropdown
against another CDS view, and `@Consumption.filterable: false` hides a
field from the filter bar even though it's still selectable.
`@Search` annotations (specifically `@Search.searchable` on the view
and `@Search.defaultSearchElement` on a field) turn on the free-text
search box in a Fiori list report and say which fields that search
actually scans, instead of the user having to know your field names
and use the filter bar for everything. In classic ABAP terms, this is
roughly the metadata that used to live scattered across a SAP GUI
selection screen, a search help, and hand-written filter logic --
here it's declared once, next to the field it describes.

## WHAT I GOT WRONG OR FUZZY ON (fill in AFTER checking a reference)

I initially thought `@Search.searchable: true` on the view alone was
enough to make free-text search work -- it isn't; without at least one
field marked `@Search.defaultSearchElement: true`, the search box
appears in the UI but silently returns nothing, because there's no
field list to scan. I was also fuzzy on `@ObjectModel.compositionRoot`
vs. a plain `@ObjectModel` association: I'd been treating every
parent-child association as a composition, but only a composition
association cascades create/delete and shows up as a
"sub-object-node" in the generated service -- a normal association is
just a lookup/reference and doesn't cascade anything.

## HOW IT CONNECTS TO MY PORTFOLIO PROJECT

I'm annotating the root entity of my project with
`@ObjectModel.compositionRoot: true` and its line-item child with a
composition association, so deleting the header cascades to the
lines automatically instead of me writing manual cleanup logic; I'm
also adding `@Search.defaultSearchElement` to the two or three fields
a user would actually type into a search box (name, reference number)
rather than leaving every field searchable by default.
