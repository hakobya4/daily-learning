# Day 35, Task 7 -- Git: merge-base, two-dot vs three-dot diff

## THE TASK

In a SCRATCH repo (`/tmp/day35-lab`, `git init -b main`): make 2 commits on `main`, branch `feature` from the second, add 2 commits on `feature`, then add 1 more commit on `main`.

1. What does `git merge-base main feature` print, and why is it the "fork point"? How does `git merge-base --is-ancestor A B` report its answer?
2. What is the difference between `git diff main feature` (two-dot) and `git diff main...feature` (three-dot)? Which one shows only what `feature` changed since the fork?
3. How do `git log main..feature`, `git log feature..main` and `git log main...feature` differ? What does `--left-right` add?
4. How would you list the files changed on `feature` only (`--name-only`) and the summary of changes (`--stat`)?
5. What does `git merge-base --fork-point main` do differently from plain `merge-base`, and when does it matter (hint: reflog / rebased upstream)?

## WHAT I RAN

```bash
# TODO: paste the commands you ran in the scratch repo
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
