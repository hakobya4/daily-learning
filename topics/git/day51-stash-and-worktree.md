# Day 51, Task 8 -- Git: stash variants and `git worktree`

## THE TASK

In a SCRATCH area (`/tmp/day51-lab`) create a repo with a few commits and a tracked file `a.txt`, then work through the questions by actually running things.

1. Edit `a.txt` and also create an untracked `new.txt`. What does plain `git stash` save and what does it leave behind? How do `-u` (`--include-untracked`) and `-a` differ, and what does `--keep-index` do?
2. How do `git stash list`, `git stash show -p`, `git stash apply`, `git stash pop` and `git stash drop` differ? What happens to the stash when `pop` hits a conflict?
3. How do you turn a stash into a branch (`git stash branch <name>`) and why can that succeed when `apply` on the current branch conflicts?
4. What is `git worktree add ../hotfix main`? What problem does it solve compared with stashing, what rule stops you from checking out the same branch in two worktrees, and how do you clean up (`git worktree list/remove/prune`)?

## WHAT I RAN

```bash
mkdir -p /tmp/day51-lab && cd /tmp/day51-lab
git init -b main
echo one > a.txt && git add a.txt && git commit -m "c1"
echo two >> a.txt && git commit -am "c2"

# Q1: what plain stash saves vs -u / -a / --keep-index
echo three >> a.txt
echo new > new.txt
echo junk > build.log && echo '*.log' > .gitignore && git add .gitignore
git stash                 # saves a.txt change + staged .gitignore; new.txt and build.log stay
git status --short        # ?? new.txt (build.log ignored)
git stash pop
git stash -u              # also takes new.txt; build.log (ignored) stays
git stash pop
git stash -a              # takes new.txt AND build.log
git stash pop
git add a.txt
git stash --keep-index    # stashes everything, but leaves the staged a.txt change in the index/worktree
git stash pop

# Q2: list / show / apply / pop / drop, and pop on conflict
git stash
git stash list            # stash@{0}: WIP on main: ...
git stash show -p stash@{0}
git stash apply           # applies, stash@{0} still in the list
git checkout -- a.txt
echo conflicting > a.txt && git commit -am "c3 conflicting"
git stash pop             # CONFLICT in a.txt -> stash is NOT dropped
git stash list            # still there
git checkout -- . 2>/dev/null; git reset --hard

# Q3: stash -> branch
git stash branch from-stash   # new branch at the stash's base commit (c2), applies, drops
git log --oneline -1
git switch main

# Q4: worktrees
git worktree add ../day51-hotfix -b hotfix main
git worktree list
git worktree add ../day51-again main      # fatal: 'main' is already checked out at '/tmp/day51-lab'
git worktree remove ../day51-hotfix
git worktree prune
```

## MY ANSWERS

1. Plain `git stash` (= `git stash push`) saves the changes to **tracked** files, both staged and unstaged, as a stash commit and resets the working tree and index to `HEAD`. Untracked files (`new.txt`) and ignored files are left behind in the working tree. `-u` / `--include-untracked` also stashes untracked files and removes them from the tree, but still leaves ignored files alone. `-a` / `--all` stashes untracked **and** ignored files (so build output like `build.log` disappears too -- use it carefully). `--keep-index` stashes everything as usual but leaves whatever is already staged in place in the index and working tree, which is handy for testing exactly what you are about to commit; note the stash still contains the staged changes as well.

2. `git stash list` shows the stack (`stash@{0}` is the newest). `git stash show` prints a diffstat of a stash, `-p` the full patch. `git stash apply [stash@{n}]` applies a stash and keeps it in the list; `git stash pop` applies and then drops it; `git stash drop [stash@{n}]` deletes one without applying (`git stash clear` deletes all). If `pop` hits a conflict, Git leaves conflict markers in the files and does **not** drop the stash -- you resolve the conflict (or `git reset --hard` to back out), then `git stash drop` it yourself once you are happy.

3. `git stash branch <name> [stash@{n}]` creates a new branch starting at the commit the stash was made on, checks it out, applies the stash there and drops it if it applied cleanly. It succeeds where `apply` on the current branch conflicts because the stash is replayed onto exactly the base it was recorded against, so there are no intervening commits (like my `c3 conflicting`) for it to clash with. You can then commit on that branch and merge/rebase later, resolving conflicts in the normal way.

4. `git worktree add ../hotfix main` creates a second working directory `../hotfix`, linked to the same repository (shared objects and refs), with `main` checked out there. Instead of stashing half-finished work, switching branches, fixing, and popping, you just `cd ../hotfix`, fix and commit, while your original directory stays untouched (including untracked files and build state). The rule: a branch can be checked out in only one worktree at a time -- `git worktree add ../x main` while `main` is checked out elsewhere fails with "already checked out" (use a new branch with `-b`, `--detach`, or `--force` if you really mean it). Clean up with `git worktree list` (see them), `git worktree remove <path>` (delete a clean worktree; `--force` if it has changes), and `git worktree prune` (forget metadata for worktrees whose directories were deleted manually).
