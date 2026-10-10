# Day 20, Task 7 -- Git: `--first-parent`, `format-patch`/`am`, `revert -m`, `switch --orphan`

## THE TASK

In a SCRATCH repo (`/tmp/fp-lab`, `git init -b main`):

1. Create a `feature` branch with 2 commits, merge it into `main` with `git merge --no-ff`, then add one more commit on `main`. What does `git log --oneline --graph` show, and how does `git log --first-parent` change the picture?
2. Undo the merge with `git revert -m 1 <merge-sha>`. Why is `-m` required, and what does `1` mean?
3. Export the last 2 commits with `git format-patch -2`, then in a second scratch repo apply them with `git am`. What is preserved that `git apply` would lose?
4. What does `git switch --orphan docs` do, and when would you want an orphan branch?
5. After the revert, what happens if you try to merge `feature` again, and how do you get its changes back?

## WHAT I RAN

```
(fill in the exact commands you ran)
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
