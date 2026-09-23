# Day 3, Task 6 -- Git: stash and rebase practice

## THE TASK

Practice two things Day 2's branch exercise didn't cover: stashing
in-progress work, and rebasing a feature branch onto an updated main.

1. Make a small change to any file (e.g. add a comment somewhere) --
   don't commit it yet.
2. Run `git stash` to shelve it, confirm with `git status` that your
   working tree is clean again.
3. Create a branch off main: `git checkout -b day3-practice`.
4. Make 2-3 small commits on that branch (anything -- even editing
   this file's checklist below counts).
5. Switch back to main, make one unrelated commit directly on main
   (or note that main genuinely didn't move today, if that's the
   case).
6. Switch back to `day3-practice` and run `git rebase main`, resolving
   any conflict if one comes up.
7. Run `git stash pop` to bring back the change from step 1, and
   decide what to do with it (commit it or discard it).
8. Merge `day3-practice` back into main and push.

## WHAT I RAN

TODO: paste the actual commands you ran, in order, once you've done
the steps above -- not the list above, your real terminal history.

## WHAT STASH AND REBASE ARE ACTUALLY FOR (write AFTER doing the steps)

TODO: one or two sentences each -- when would you reach for `git
stash` vs just committing a WIP commit? When would you rebase a
branch instead of merging main into it?
