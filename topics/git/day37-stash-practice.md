# Day 37, Task 7 -- Git: stash, partial stash and applying elsewhere

## THE TASK

In a SCRATCH repo (`/tmp/day37-lab`, `git init -b main`): make one commit with two files, edit both, and practice stashing.

1. What does `git stash` save by default, and what does it NOT save (untracked/ignored files)? Which flags change that?
2. How do you stash only ONE of two modified files (or only some hunks)?
3. What is the difference between `git stash apply` and `git stash pop`? What happens on a conflict with `pop`?
4. How do you list stashes, show the diff of `stash@{1}`, and turn a stash into a new branch?
5. You stashed on `main` but want those changes on another branch -- how, and what is `git stash drop` / `git stash clear`?

## WHAT I RAN

```bash
mkdir /tmp/day37-lab && cd /tmp/day37-lab && git init -b main
echo one > a.txt && echo one > b.txt && git add . && git commit -m "init"
echo two >> a.txt && echo two >> b.txt && echo new > c.txt
git stash                      # saves tracked changes only; c.txt stays
git stash list
git stash push -u -m "with untracked"   # -u includes untracked, -a also ignored
git stash push -m "only a" -- a.txt     # stash a single file
git stash push -p                       # choose hunks interactively
git stash show -p stash@{1}
git stash apply                # keep stash
git stash pop                  # apply + drop
git stash branch fix-branch stash@{0}   # new branch from stash
git stash drop stash@{0}; git stash clear
```

## MY ANSWERS

1. `git stash` saves modified and staged tracked files (index + working tree changes) and resets the tree to HEAD. It does not save untracked or ignored files. `-u` / `--include-untracked` adds untracked files; `-a` / `--all` adds ignored files too.
2. Use a pathspec: `git stash push -- a.txt` stashes only that file. `git stash push -p` lets you pick individual hunks interactively. `--keep-index` leaves staged changes in place.
3. `apply` re-applies the stash and keeps it in the stash list; `pop` applies and then drops it. If `pop` hits a conflict, the changes are left conflicted in the working tree and the stash is NOT dropped, so you resolve the conflict and drop it manually.
4. `git stash list` lists stashes; `git stash show -p stash@{1}` shows the diff of that stash; `git stash branch <name> [stash@{n}]` creates a new branch from the commit the stash was made on, applies the stash and drops it.
5. Switch to the other branch and run `git stash apply stash@{n}` (or `pop`); conflicts are possible if the branches diverged. `git stash drop [stash@{n}]` deletes one stash; `git stash clear` deletes all of them.
