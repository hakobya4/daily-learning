# Day 54, Task 9 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: CDS table functions backed by AMDP (`DEFINE TABLE FUNCTION ... IMPLEMENTED BY METHOD`, the `FOR TABLE FUNCTION` AMDP method written in SQLScript, and when you would reach for one instead of a normal CDS view), the RAP `precheck` handler (`precheck` on create/update in the behavior definition, how it differs from a validation and why it runs BEFORE data reaches the transactional buffer), or ABAP Cloud release contracts (released APIs, the C1/C0 contracts, why `SELECT FROM mara` fails in a Steampunk/ABAP Cloud language version and what you use instead) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

ABAP Cloud release contracts: released APIs, the C1 / C0 contracts (and C2 / C3), and why `SELECT FROM mara` fails in the "ABAP for Cloud Development" language version.

## MY EXPLANATION (write this BEFORE looking anything up)

In classic ABAP you can touch anything in the system: `SELECT * FROM mara`, call any function module, read any SAP class, even enhance standard code. That is convenient, but it is also why upgrades are painful -- SAP never promised that `MARA`'s fields, or the internals of some function module, stay the same, so every upgrade can break custom code that relied on them.

ABAP Cloud (SAP BTP ABAP Environment, "Steampunk", and the "Developer extensibility" side of S/4HANA) flips that around. Your code is compiled with the restricted language version **ABAP for Cloud Development**, and in that version you may only use:

- a restricted ABAP language subset (no `CALL TRANSACTION`, no classic dynpro / `WRITE` lists, no `CALL FUNCTION ... DESTINATION` to random systems, no native SQL, etc.), and
- SAP objects that are explicitly **released** for that use -- tables, CDS views, classes, interfaces, BAdIs, data elements.

"Released" is a **release contract**: SAP marks an object with a contract and promises to keep it stable across upgrades (no incompatible changes; if it has to go, it is deprecated first with a successor). The contracts I remember:

- **C1 -- use system-internally**: the object may be *used* by your code inside the same system (read a released CDS view, call a released class, use a released data element). This is what most "released APIs" are.
- **C0 -- extend**: the object is stable as an *extension point*, e.g. a CDS view or behavior definition that you are allowed to add fields/behavior to via extensions, or a BAdI you can implement. SAP promises not to break your extension.
- **C2 -- use as remote API**: stable for remote consumption (OData/SOAP services exposed via communication scenarios), relevant for side-by-side apps.
- **C3** -- for configuration/authorization objects used in key-user tooling (less relevant for my code).

So why does `SELECT FROM mara` fail? `MARA` is a classic DDIC table that is **not released** (no C1 contract). When the compiler checks a class with language version ABAP for Cloud Development, it sees a reference to a non-released object and gives a syntax error ("use of MARA is not permitted"). It is not a runtime authorization error -- the code does not even activate.

What do you use instead? The **released CDS view** that SAP provides as the stable interface for that data -- for products that is `I_Product` (with associations like `_Text`, `_Plant`, ...). Released objects are usually the "I_" interface views of the Virtual Data Model. So:

```abap
" classic -- not allowed in ABAP Cloud
SELECT matnr, mtart FROM mara INTO TABLE @DATA(lt_mat) UP TO 10 ROWS.

" ABAP Cloud -- released C1 CDS view instead
SELECT Product, ProductType FROM I_Product INTO TABLE @DATA(lt_prod) UP TO 10 ROWS.
```

The same rule applies to everything else: instead of `BAPI_...` function modules you use released RAP business objects through EML (`MODIFY ENTITIES OF I_...`), instead of `sy-datum` style tricks you use released classes like `cl_abap_context_info=>get_system_date( )`, instead of `WRITE` you output via `if_oo_adt_classrun~main` and `out->write( )` in ADT.

How do you find what is released? In ADT, the object's **Properties -> API State** tab shows its contract; there is also the "Released Objects" tree in the Project Explorer, and SAP publishes the list (and successor information for unreleased objects -- e.g. "use I_Product instead of MARA") on GitHub / via the Cloudification Repository. If nothing released fits, in S/4HANA on-prem / private cloud you can wrap the unreleased thing in your own class written in "Standard ABAP" (tier 2 in the 3-tier extensibility model), release *that* wrapper for cloud development yourself, and use it from your cloud-ready code -- but on BTP ABAP Environment that escape hatch does not exist.

The big idea for a classic ABAPer: you trade "I can call anything" for "SAP guarantees what I call won't break on upgrade". That is what makes clean-core extensions upgrade-safe.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

- I had the numbering right but should be precise on wording: SAP describes C0 as the contract for **extension** ("stable extension points"), C1 for **system-internal use**, C2 for **remote API use**; C3 relates to manage configuration content / authorization defaults. Several objects carry more than one contract (a CDS view can be released for both C0 and C1).
- The check happens at **design/compile time** through the language version (and the ATC "cloud readiness" checks for Standard ABAP code), not at runtime -- so you find the problem when activating, which is what makes it enforceable.
- Release state can be "Released", "Deprecated" (still usable but with a warning and a named successor) or "Not to be released". Deprecated objects keep working for a while, so migrating is not urgent but should be planned.
- The 3-tier model (tier 1 = ABAP Cloud, tier 2 = "cloud API enablement" wrappers in classic ABAP, tier 3 = classic extensions) is the official answer to "what if there is no released API yet" in S/4HANA private cloud / on-prem; SAP's newer guidance folds this into "clean core" levels, but the principle is the same: keep the unreleased access in one small, clearly marked wrapper.
