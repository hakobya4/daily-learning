# Day 10, Task 6 -- Git: stash variants and `git clean`

## THE TASK

Earlier days used worktrees, reflog, bisect and tags. This one covers
shelving work with `git stash` (beyond the basic push/pop) and removing
untracked files safely with `git clean`.

1. In a SCRATCH repo (`/tmp/stash-practice`, `git init -b main`), make a
   commit with `a.txt` and `b.txt`.
2. Edit a.txt (tracked), `git add` a NEW file `c.txt` (staged), and
   create an untracked `notes.tmp` plus an ignored `build.log`
   (add `*.log` to .gitignore first).
3. Run plain `git stash`. What happened to each of the four kinds of
   change? Then `git stash list`.
4. Recreate the situation and use `git stash push -u -m "wip"`, then
   `git stash push --keep-index`, and note the differences.
5. Restore with `git stash apply` vs `git stash pop`; which one keeps
   the entry? Try `git stash branch fix-x stash@{0}`.
6. Use `git clean -n`, then `git clean -fd`, then `git clean -fdx`.
   What does each remove? Why is `-n` first?

## WHAT I RAN

(fill in the commands and their output)

## WHAT EACH KIND OF CHANGE DID (write AFTER)

- tracked + modified:
- staged new file:
- untracked file:
- ignored file:

## STASH vs COMMIT-ON-A-WIP-BRANCH (write in your own words)

TODO
