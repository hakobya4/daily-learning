# Day 19, Task 7 -- Git: `bisect run`, `git notes`, `commit --fixup`, `blame -L`

## THE TASK

In a SCRATCH repo (`/tmp/bisect-lab`, `git init -b main`):

1. Make 8 commits that append a line to `f.txt`; make commit 5 add the line `BUG`. Write a script `check.sh` (outside the repo) that exits 1 if `f.txt` contains `BUG`, else 0.
2. Use `git bisect start`, `git bisect bad HEAD`, `git bisect good <first commit>` and `git bisect run ../check.sh` to find the first bad commit automatically. What does the output look like and how do you end the session?
3. Attach a note to a commit with `git notes add -m "..." <commit>`. How do you show it in `git log`, and why do notes not change the commit hash?
4. Fix a typo in an earlier commit's file using `git commit --fixup <commit>` and then `git rebase -i --autosquash`. What does the fixup commit message look like before the autosquash?
5. What does `git blame -L 3,5 f.txt` show, and how do you ignore a pure-formatting commit with `--ignore-rev`?

## WHAT I RAN

```
(TODO: paste the commands you actually ran)
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
