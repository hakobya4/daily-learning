# Day 13, Task 6 -- Git: merge conflicts, --ours/--theirs, and merge vs. rebase

## THE TASK

In a SCRATCH repo (`/tmp/merge-lab`, `git init -b main`):

1. Commit `app.txt` with three lines (`alpha`, `beta`, `gamma`) on main.
2. Branch `feature`; change line 2 to `beta-feature` and commit. Back on
   main change line 2 to `beta-main` and commit.
3. Merge `feature` into main. What does the conflict marker block look
   like? Resolve it by hand, then `git add` and `git commit`.
4. Abort/redo the merge (`git merge --abort`, `git reset --hard
   HEAD~1` as needed) and try `git merge -X theirs feature`. How does
   `-X theirs` differ from `git merge -s ours feature`?
5. Redo the scenario but integrate with `git rebase main` from
   `feature`. In a rebase, which side is "ours" and which is "theirs"?
   Why does it feel reversed?
6. Enable `git config rerere.enabled true` in the scratch repo and
   explain what it remembers.

## WHAT I RAN

TODO: paste the commands you actually ran.

## WHAT EACH COMMAND SHOWED (write AFTER)

TODO: conflict markers, how `-X theirs` and `-s ours` differ, which
side is which during a rebase, what rerere stored.

## WHEN I WOULD USE EACH (write in your own words)

TODO: merge commit vs. rebase vs. `-X` options on a team branch.
