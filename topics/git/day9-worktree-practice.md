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

```
mkdir /tmp/wt-practice && cd /tmp/wt-practice && git init -b main
echo v1 > app.txt && git add app.txt && git commit -m "v1"
echo v2 > app.txt && git commit -am "v2"
git branch hotfix
git worktree add ../wt-hotfix hotfix
# in ../wt-hotfix: echo hotfix > app.txt && git commit -am "hotfix fix"
# in main folder:  echo wip >> app.txt   (left uncommitted)
git worktree list
#   /tmp/wt-practice  <sha> [main]
#   /tmp/wt-hotfix    <sha> [hotfix]
git checkout hotfix
#   fatal: 'hotfix' is already checked out at '/tmp/wt-hotfix'
git restore app.txt                     # working tree back to HEAD (wip gone)
git restore --source=HEAD~1 app.txt     # working tree now has v1, unstaged
git add app.txt && git restore --staged app.txt   # unstage only; file content kept
git worktree remove ../wt-hotfix && git worktree prune
```

Key observations: each worktree has its own working files and index, so
the uncommitted `wip` edit in the main folder was untouched by the
commit made in `wt-hotfix`, and vice versa.

## WHY WORKTREES INSTEAD OF STASH?

A worktree is a second checked-out folder that shares the same
repository (objects, branches, reflog). With stash I have to shelve my
half-done work, switch branches, fix, switch back and pop, and I can hit
conflicts on pop or forget the stash. With a worktree my unfinished
work stays exactly where it is while I do the hotfix in another folder;
I can even run both builds/tests at once. Git refuses to check out
`hotfix` in the main folder because a branch may be checked out in only
one worktree at a time -- two working folders moving the same branch
ref would silently desync each other's index and HEAD.

## `git restore` vs `git restore --staged` vs `--source` (write AFTER)

- `git restore <file>`: overwrite the working-tree file with the version
  in the index (staged, else HEAD). Discards unstaged edits -- not
  recoverable.
- `git restore --staged <file>`: only touches the index; copies HEAD's
  version into the index, i.e. unstages. The working-tree content is
  left alone, so no work is lost.
- `git restore --source=<commit> <file>`: take the content from that
  commit instead of the index/HEAD (e.g. `HEAD~1`) and put it in the
  working tree (add `--staged` too to also update the index).
