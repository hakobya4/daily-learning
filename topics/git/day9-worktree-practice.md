# Day 9, Task 7 -- Git: worktrees and `git restore`

## THE TASK

Days 2-8 covered branching, rebase, cherry-pick, bisect, reflog and
tags. This one is about working on two branches at the same time
WITHOUT stashing, using `git worktree`, plus undoing changes with
`git restore`.

1. In a SCRATCH repo: `mkdir /tmp/wt-practice && cd /tmp/wt-practice && git init`,
   make 2 commits on main (a file `app.txt`).
2. Create a branch `hotfix` and add a NEW worktree for it in a sibling
   folder: `git worktree add ../wt-hotfix hotfix`.
3. In `../wt-hotfix` change app.txt and commit. Meanwhile in the main
   folder leave an UNCOMMITTED edit to app.txt. Confirm neither
   working folder disturbed the other.
4. Run `git worktree list`. Then try `git checkout hotfix` in the main
   folder and read the error -- why does git refuse?
5. Discard the uncommitted edit in the main folder with
   `git restore app.txt`; then try `git restore --source=HEAD~1 app.txt`
   and `git restore --staged` after `git add` to see the difference
   between working-tree restore and index restore.
6. Clean up: `git worktree remove ../wt-hotfix`, `git worktree prune`.

## WHAT I RAN

TODO: paste your commands and the key output here.

## WHY WORKTREES INSTEAD OF STASH? (write AFTER doing the steps)

TODO

## `git restore` vs `git restore --staged` vs `--source` (write AFTER)

TODO
