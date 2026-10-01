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

```
mkdir /tmp/stash-practice && cd /tmp/stash-practice && git init -b main
echo a > a.txt && echo b > b.txt && echo '*.log' > .gitignore
git add . && git commit -m "init"
echo changed >> a.txt          # tracked, modified
echo c > c.txt && git add c.txt # staged new file
echo n > notes.tmp              # untracked
echo l > build.log              # ignored
git stash                       # saves a.txt change + staged c.txt
git status --short              # ?? notes.tmp  (untracked stays; ignored stays)
git stash list                  # stash@{0}: WIP on main: <sha> init
git stash pop
git stash push -u -m "wip"      # now notes.tmp is stashed too (ignored still not)
git stash pop
git stash push --keep-index     # stashes, but staged c.txt stays in index + working tree
git stash apply                 # re-applies, KEEPS the stash entry
git stash drop
git stash pop                   # re-applies and REMOVES the entry on success
git stash branch fix-x stash@{0}  # new branch from the stash's base commit, applies + drops it
git clean -n                    # dry run: "Would remove notes.tmp"
git clean -fd                   # removes untracked files and dirs, keeps ignored
git clean -fdx                  # also removes ignored files (build.log)
```

## WHAT EACH KIND OF CHANGE DID (write AFTER)

- tracked + modified: stashed by plain `git stash`; working tree reverts to HEAD.
- staged new file: also stashed (index state is saved); c.txt disappears from the working tree.
- untracked file: NOT stashed by default; it stays put. `-u` includes it.
- ignored file: NOT stashed even with `-u`; only `-a` (--all) includes ignored files.

Other notes: `--keep-index` stashes everything but leaves staged changes
in the index and working tree, handy for testing exactly what you are
about to commit. `apply` keeps the stash entry, `pop` removes it (unless
there was a conflict). `git stash branch` is the clean way out when a
pop would conflict: it checks out the commit the stash was made on, so
the apply is conflict-free. `git clean -n` is a dry run and goes first
because `clean` deletes files that git has no copy of, so it cannot be
undone; `-fd` adds directories, `-x` adds ignored files such as build
output.

## STASH vs COMMIT-ON-A-WIP-BRANCH (write in your own words)

A stash is a quick, private, unnamed shelf: good for a few minutes of
"let me look at something else" and for changes I don't want in history.
It is easy to forget (stash entries have no branch name and pile up) and
untracked files are skipped unless I remember `-u`. A WIP commit on a
branch is visible, named, backed up if I push it, and can be amended or
squashed later, so I use it when the interruption will last hours or
days. Rule of thumb: stash for minutes, WIP branch for anything longer.
