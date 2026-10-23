# Day 32, Task 7 -- Git: `stash` variants, `clean`, `worktree prune`-free cleanup, `restore -p`

## THE TASK

In a SCRATCH repo (`/tmp/day32-lab`, `git init -b main`) with one commit containing `a.txt` and `b.txt`, then local edits to both plus an untracked `new.txt` and an ignored `junk.log` (`*.log` in `.gitignore`):

1. How do you stash ONLY the tracked changes, and how do you also stash untracked files (`-u`) or even ignored ones (`-a`)? What does each leave in the working tree?
2. How do you stash just ONE file (`git stash push -- <path>`) and give the stash a message (`-m`)? How do you list stashes?
3. What is the difference between `git stash apply` and `git stash pop`, and how do you restore a stash onto a NEW branch in one step (`git stash branch`)?
4. How do you preview what `git clean` would delete (`-n`), delete untracked files and directories (`-fd`), and also remove ignored files (`-x`)? Why does clean refuse to run without `-f`?
5. How do you interactively discard only some hunks of a file (`git restore -p`) and how is that different from `git restore <file>`?

## WHAT I RAN

```bash
rm -rf /tmp/day32-lab && mkdir /tmp/day32-lab && cd /tmp/day32-lab
git init -b main
echo '*.log' > .gitignore; echo a > a.txt; echo b > b.txt
git add . && git commit -m init
echo a2 >> a.txt; echo b2 >> b.txt; echo n > new.txt; echo j > junk.log

git stash && git status --short && git stash pop      # tracked only
git stash -u && ls && git stash pop                   # + untracked
git stash -a && ls -a && git stash pop                # + ignored too
git stash push -m "only a" -- a.txt && git status --short
git stash list
git stash apply && git stash drop
git stash branch fix-branch                           # new branch from stash
git clean -n                                          # dry run
git clean -nx                                         # dry run incl. ignored
git clean -fd                                         # delete untracked files/dirs
git clean -fdx                                        # also ignored files
git restore -p a.txt                                  # interactive hunks
```

## MY ANSWERS

1. Plain `git stash` saves only changes to tracked files (staged and unstaged) and resets them to HEAD; `new.txt` (untracked) and `junk.log` (ignored) stay in the working tree. `git stash -u` also stashes untracked files, so `new.txt` disappears but `junk.log` stays. `git stash -a` (`--all`) stashes ignored files as well, so `junk.log` is gone too and the tree is fully clean.
2. `git stash push -m "only a" -- a.txt` stashes just that path with a message; `b.txt` stays modified. `git stash list` shows entries like `stash@{0}: On main: only a`.
3. `git stash apply` re-applies the stash and keeps it in the list; `git stash pop` applies it and drops it if it applied cleanly (on a conflict it is kept). `git stash branch <name> [stash]` creates a new branch at the commit the stash was made from, checks it out, applies the stash and drops it, which avoids conflicts when the original branch has moved on.
4. `git clean -n` (dry run) lists what would be removed ("Would remove new.txt"); `git clean -fd` deletes untracked files and directories; adding `-x` also removes ignored files (`junk.log`); `-X` removes only ignored files. Clean refuses without `-f` (when `clean.requireForce` is true, the default) because deletions are permanent: untracked files are not in any commit, so there is no way to get them back.
5. `git restore -p <file>` walks through each hunk and asks (y/n/s to split/e to edit) whether to discard it from the working tree, so you keep some edits and throw away others. `git restore <file>` discards ALL unstaged changes in that file at once, without asking.
