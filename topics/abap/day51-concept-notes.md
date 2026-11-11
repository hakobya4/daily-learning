# Day 51, Task 9 (ABAP slot) -- ABAP/RAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: RAP actions vs functions (`action`/`function` in the behavior definition, `result [1] $self`, instance vs static, `%cid`/`%tky` keys in the handler), the RAP business object `EML` (`READ ENTITIES`, `MODIFY ENTITIES`, `COMMIT ENTITIES` and the `FAILED`/`REPORTED` response structures), or CDS access control (`DEFINE ROLE`, `GRANT SELECT ... WHERE`, and what happens without a DCL) -- and explain it as if teaching a classmate who knows classic ABAP report programs and BAPIs but has never touched RAP.

## CONCEPT CHOSEN

Determine actions in RAP (`determine action` in the behavior definition) -- running selected determinations and validations on demand, before save.

## MY EXPLANATION (write this BEFORE looking anything up)

Normally in RAP, validations only run in the save phase (`on save`), so a user filling a Fiori form only finds out the data is wrong when they press Save. Think of a classic dialog transaction where the PAI checks only fire at the very end -- annoying for long forms. A determine action fixes this: it is a named bundle of existing determinations and validations that a client can trigger explicitly at any time during the interaction phase.

In the behavior definition you declare it like this:

```
determine action checkDates
{
  validation validateDates;
  validation validateCustomer;
  determination calculateTotal;
}
```

There is no handler method to write for the action itself -- the framework just executes the listed validations and determinations for the given instances, as if their triggers had fired, and fills `failed` / `reported` with any messages. You expose it in the projection with `use action checkDates;`, and the Fiori UI can call it (for example via side effects or a button) so messages appear while the user is still editing. From ABAP you call it through EML, `MODIFY ENTITIES OF zi_travel ENTITY Travel EXECUTE checkDates FROM VALUE #( ( %tky = ... ) )`.

The most important use case is draft: the framework itself has the built-in determine action `Prepare`, which runs the validations listed under `draft determine action Prepare { ... }` before a draft is activated. So with draft, `Prepare` is basically "run my checks now", and `Activate` only succeeds if they pass.

## WHAT I GOT WRONG / LEARNED AFTER CHECKING

Points to keep straight: a determine action may only list determinations that are `on save` and validations of the same BO (determinations `on modify` already run immediately, so they make no sense there); you can also include validations/determinations of child entities with the `Child ~ validationName` syntax. Running a determine action does not save anything -- it only touches the transactional buffer, and the regular save sequence still runs all `on save` validations again at the end. `Prepare` only exists for draft-enabled BOs, and if you do not list your validations inside `draft determine action Prepare`, they will not run when the Fiori draft is activated until the final save, which is a common reason messages "only show up late".
