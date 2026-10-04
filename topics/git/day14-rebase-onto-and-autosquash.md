# Day 14, Task 6 -- Git: fixup commits, --autosquash, and rebase --onto

## THE TASK

Day 4 covered interactive squash and Day 3 plain rebase. This one is
about two sharper tools: `commit --fixup` with `rebase --autosquash`,
and `rebase --onto` for moving a branch off the wrong base.

In a SCRATCH repo (`/tmp/onto-lab`, `git init -b main`):

1. Commit `a.txt` ("base") on main.
2. Branch `topic` and make three commits: `t1`, `t2`, `t3` (each adds a
   line to `topic.txt`).
3. You notice a typo in the line added by `t1`. Fix it and record it with
   `git commit --fixup <sha-of-t1>`. What does the new commit's message
   look like?
4. Run `git rebase -i --autosquash main` (use `GIT_SEQUENCE_EDITOR=true`
   to accept the todo list as-is). What did autosquash reorder, and what
   does `git log --oneline` show now?
5. Create `feature` branched from `topic` (so it holds topic's commits)
   plus one extra commit `f1`. Later you decide `feature` should NOT
   depend on topic's commits but only on `f1`: move it onto main with
   `git rebase --onto main topic feature`. Explain the three arguments
   (newbase, upstream, branch) in your own words.
6. Compare the old and new `feature` with `git range-diff`. When would
   that be useful?

## WHAT I RAN

(paste the exact commands, TODO)

## WHAT EACH COMMAND SHOWED (write AFTER)

- TODO: fixup commit message and what autosquash did
- TODO: what `--onto` moved and what it left behind
- TODO: what range-diff reports

## WHEN I WOULD USE EACH (write in your own words)

TODO
