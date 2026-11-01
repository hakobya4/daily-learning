# Day 41, Task 7 -- Git: bisect, reflog recovery and worktrees

## THE TASK

In a SCRATCH area (`/tmp/day41-lab`) create a repo with ~10 commits where a test
script starts failing at some middle commit.

1. How do you find the first bad commit with `git bisect`? Give the start commands, and how `git bisect run ./test.sh` decides good/bad/skip (exit codes). How do you end the session?
2. You ran `git reset --hard HEAD~3` by mistake. How do you get the commits back using the reflog? What is the difference between `HEAD@{2}` and `HEAD~2`?
3. What is `git worktree add ../hotfix main` for, and what restriction applies to the same branch in two worktrees?
4. What does `git reflog expire` / `git gc` do to "lost" commits, and roughly how long do unreachable commits survive by default?
5. Difference between `git restore --staged f` and `git restore f`.

## WHAT I RAN

```bash
# TODO: paste the commands you actually ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
