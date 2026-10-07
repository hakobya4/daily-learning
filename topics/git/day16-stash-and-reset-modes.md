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
git init -b main                      # in /tmp/reset-lab
echo A >> log.txt; git add log.txt; git commit -m A     # then B, then C
echo wip >> log.txt
git stash push -m "wip"               # tracked edit saved, worktree clean
echo hi > new.txt
git stash                             # "No local changes to save" -- new.txt ignored
git stash -u -m "wip-u"               # -u / --include-untracked saves new.txt too
git stash list                        # stash@{0}: wip-u, stash@{1}: wip
git stash pop                         # restores the newest stash, drops it
git reset --soft HEAD~1               # status: "M  log.txt" (staged)
git commit -m C
git reset --mixed HEAD~1              # status: " M log.txt" (unstaged)
git add log.txt; git commit -m C
git reset --hard HEAD~1               # status clean, log shows only A, B
git reflog                            # HEAD@{1}: commit: C
git reset --hard HEAD@{1}             # C is back
```

## MY ANSWERS

1. Setup: three commits A, B, C, each appending a line to `log.txt`.
2. A plain `git stash` saves tracked changes (staged and unstaged) but NOT
   untracked files: with only `new.txt` present it said "No local changes
   to save". `git stash -u` (`--include-untracked`) includes them (`-a`
   adds ignored files too). `git stash pop` re-applies the newest stash
   and drops it from the list.
3. `--soft`: HEAD moves back one commit, but the index and worktree are
   untouched, so C's changes end up STAGED (index). Just commit again.
4. `--mixed` (default): HEAD moves and the index is reset to match, but
   the worktree keeps the files, so C's changes end up as UNSTAGED edits
   in the worktree.
5. `--hard`: HEAD, index and worktree all move, so C's changes are gone
   from the working tree. The commit still exists as an unreachable
   object: `git reflog` shows it (`HEAD@{1}`) and
   `git reset --hard HEAD@{1}` (or `git branch rescue <sha>`) brings it
   back until garbage collection prunes it.
6. `reset --hard` overwrites tracked files in the worktree and index
   without asking. Uncommitted edits were never in any commit, so they
   are not in the reflog and cannot be recovered. `git stash` first
   records them as a commit, so they survive the hard reset and can be
   brought back with `git stash pop`.
