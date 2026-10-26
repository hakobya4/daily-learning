# Day 36, Task 7 -- Git: reflog and recovering lost commits

## THE TASK

In a SCRATCH repo (`/tmp/day36-lab`, `git init -b main`): make 3 commits, then run `git reset --hard HEAD~2` and later recover the lost commits.

1. What is the reflog, how does it differ from `git log`, and how long do entries live by default?
2. After `git reset --hard HEAD~2`, how do you find the SHA of the commit you lost, and how do you get back to it (two ways)?
3. What does `HEAD@{1}` mean vs `HEAD~1`? What does `main@{yesterday}` do?
4. You deleted a branch with `git branch -D topic`. How do you bring it back?
5. What do `git fsck --lost-found` and `git gc --prune=now` have to do with unreachable commits?

## WHAT I RAN

```bash
rm -rf /tmp/day36-lab && mkdir /tmp/day36-lab && cd /tmp/day36-lab
git init -b main
# TODO: fill in the commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
