# Day 22, Task 7 -- Git: `revert -m`, `commit --fixup`, `reflog expire`, `git notes`

## THE TASK

In a SCRATCH repo (`/tmp/revert-lab`, `git init -b main`):

1. Create `feature`, add two commits, merge it into `main` with `--no-ff`. How do you undo that merge with a new commit (`git revert -m ?`) and why must you give `-m`? What does `-m 1` mean?
2. After that revert, you merge `feature` again and nothing comes in. Why, and how do you get the changes back (revert the revert, or a different approach)?
3. Make a typo commit on `main`, then more commits after it. How do you create a `fixup!` commit for the typo commit and fold it in with `git rebase -i --autosquash`? What does `git commit --fixup=amend:<sha>` add?
4. Attach a note to a commit with `git notes add`. Do notes travel on a normal `git push`? How do you push/fetch them?
5. After a bad rebase you want to permanently drop old reflog entries: which `git reflog expire` and `git gc` flags do that, and why is it dangerous?

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
