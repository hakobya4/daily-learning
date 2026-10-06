# Day 16, Task 7 -- Git: stash, and the three modes of reset

## THE TASK

In a SCRATCH repo (`/tmp/reset-lab`, `git init -b main`):

1. Make three commits A, B, C, each adding a line to `log.txt`.
2. Edit `log.txt` (uncommitted) and `git stash push -m "wip"`. Then add an
   untracked file `new.txt`. Which of the two does a plain `git stash`
   NOT save? Which flag includes it? Restore with `git stash pop`.
3. `git reset --soft HEAD~1`: where do commit C's changes end up
   (index / worktree / gone)? Re-commit.
4. `git reset --mixed HEAD~1` (the default): same question.
5. `git reset --hard HEAD~1`: same question. How do you get C back
   afterwards (hint: reflog)?
6. Why is `git reset --hard` dangerous with uncommitted work, but
   `git stash` + `git reset --hard` is safe?

## WHAT I RAN

```
TODO
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
6. TODO
