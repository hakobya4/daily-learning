# Day 47, Task 7 -- Git: gc, prune, fsck and unreachable objects

## THE TASK

In a SCRATCH area (`/tmp/day47-lab`) create a repo and work through the questions by actually running things.

1. Make 3 commits, then `git reset --hard HEAD~1`. Is the dropped commit gone? Which command lists it (`git fsck --lost-found` / `--unreachable`) and which keeps it reachable (hint: reflog)?
2. Expire the reflog (`git reflog expire --expire=now --all`) and run `git gc --prune=now`. What happens to the dropped commit and why would a plain `git gc` not remove it right away (hint: `gc.pruneExpire`)?
3. What is the difference between `git gc`, `git prune` and `git repack -ad`? What does a packfile buy you over loose objects?
4. What does `git fsck` report for a dangling blob vs a dangling commit, and how can you recover a dangling commit by hash?

## WHAT I RAN

```bash
# TODO: paste the commands you actually ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
