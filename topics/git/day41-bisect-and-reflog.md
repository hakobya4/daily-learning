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
mkdir -p /tmp/day41-lab && cd /tmp/day41-lab && git init -q
for i in $(seq 1 10); do echo $i > n.txt; [ $i -ge 6 ] && echo bad > flag.txt; git add .; git commit -qm "c$i"; done
printf '#!/bin/sh\n! test -f flag.txt\n' > test.sh && chmod +x test.sh   # untracked, survives checkouts
git bisect start
git bisect bad HEAD
git bisect good HEAD~9
git bisect run ./test.sh
git bisect reset
git reset --hard HEAD~3
git reflog
git reset --hard 'HEAD@{1}'
git worktree add ../hotfix main      # fails if main is already checked out here
git restore --staged n.txt ; git restore n.txt
```

## MY ANSWERS

1. `git bisect start`, then `git bisect bad <commit>` (usually HEAD) and `git bisect good <commit>`; git checks out the midpoint each time and you mark it good/bad until it names the first bad commit (binary search, log2 N steps). `git bisect run ./test.sh` automates it: exit code 0 = good, 1-124 and 126-127 = bad, 125 = skip (can't be tested), and 128+ aborts the run. End with `git bisect reset`, which returns to the original branch.
2. `git reflog` shows where HEAD pointed before; find the entry from before the reset (for example `HEAD@{1}`) and run `git reset --hard HEAD@{1}` (or `git branch rescue <sha>`). `HEAD@{2}` means where HEAD was two moves ago (time-based, from the reflog, local only); `HEAD~2` means the second ancestor of the current commit (history-based, via parents).
3. `git worktree add ../hotfix main` checks out another working directory of the same repo, so you can work on a hotfix without stashing or cloning, sharing one object store. A branch can be checked out in only one worktree at a time (git refuses, unless `--force`); use `-b newbranch` or a detached checkout instead.
4. Unreachable commits are not deleted immediately: reflog entries keep them reachable for 90 days by default (`gc.reflogExpire`), and 30 days for entries that are themselves unreachable (`gc.reflogExpireUnreachable`). `git reflog expire` prunes those entries, and `git gc` then deletes unreachable objects older than `gc.pruneExpire` (2 weeks by default). So "lost" commits are recoverable for a while, but not forever.
5. `git restore --staged f` unstages: it copies the HEAD version of `f` into the index and leaves your working-tree edits untouched. `git restore f` discards working-tree changes by overwriting the file from the index, losing unstaged edits (not recoverable by git).
