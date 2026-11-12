# Day 52, Task 8 -- Git: stacked branches and `git rebase --update-refs`

## THE TASK

In a SCRATCH area (`/tmp/day52-lab`) create a repo with a few commits on `main`, then build a "stack" of branches: `feat-a` (2 commits) off `main`, `feat-b` (2 commits) off `feat-a`, and `feat-c` (1 commit) off `feat-b`. Add one more commit to `main`. Work through the questions by actually running things.

1. Check out `feat-c` and run a plain `git rebase main`. Where do `feat-a` and `feat-b` point afterwards (`git log --oneline --graph --all`)? Why is that a problem for stacked pull requests?
2. Reset the lab (or rebuild it) and repeat with `git rebase --update-refs main`. What happens to `feat-a` and `feat-b` now? What do the `update-ref` lines look like in `git rebase -i --update-refs main`'s todo list, and what happens if you delete one?
3. How do you make this the default (`rebase.updateRefs`)? Which branches does it NOT update (hint: a branch checked out in another worktree)?
4. Before `--update-refs` existed, how would you have fixed the stack by hand (e.g. `git rebase --onto`)? Write the exact commands for `feat-b` and `feat-c` after `feat-a` was rebased.

## WHAT I RAN

```bash
# build the stack (separate files per commit so rebases don't conflict)
mkdir -p /tmp/day52-lab && cd /tmp/day52-lab
git init -b main
c(){ echo "$1" > "$1.txt"; git add "$1.txt"; git commit -m "$1"; }
c m1; c m2
git switch -c feat-a; c a1; c a2
git switch -c feat-b; c b1; c b2
git switch -c feat-c; c c1
git switch main; c m3
git branch save-a feat-a; git branch save-b feat-b; git branch save-c feat-c   # backups to reset the lab

# Q1: plain rebase of the top of the stack
git switch feat-c
git rebase main
git log --oneline --graph --all     # feat-c moved onto m3; feat-a/feat-b still on the OLD a1..b2 off m2

# Q2: same thing with --update-refs (needs git >= 2.38)
git reset --hard save-c
git rebase --update-refs main
git log --oneline --graph --all     # feat-a and feat-b now point at the rewritten a2' / b2'
git reset --hard save-c; git branch -f feat-a save-a; git branch -f feat-b save-b
git rebase -i --update-refs main    # todo list contains "update-ref refs/heads/feat-a" lines

# Q3: make it the default
git config --global rebase.updateRefs true
git worktree add ../day52-wt feat-b # feat-b checked out elsewhere -> rebase from feat-c skips it

# Q4: the pre-2.38 manual fix with --onto
git reset --hard save-c; git branch -f feat-a save-a; git branch -f feat-b save-b
git switch feat-a && git rebase main
git rebase --onto feat-a save-a feat-b   # replay only b1,b2 (commits after OLD feat-a) onto new feat-a
git rebase --onto feat-b save-b feat-c   # replay only c1 onto new feat-b
git log --oneline --graph feat-a feat-b feat-c main   # one straight line m1..m3,a1..a2,b1..b2,c1
```

## MY ANSWERS

1. A plain `git rebase main` from `feat-c` replays all five commits (a1, a2, b1, b2, c1) onto `m3`, but it only moves the branch you are on. `feat-a` and `feat-b` keep pointing at the ORIGINAL a2 and b2, which still sit on top of `m2`. So the graph now has two copies of a1..b2: the old ones (reachable from `feat-a`/`feat-b`) and new rewritten ones (only reachable from `feat-c`). For stacked PRs that is bad: the PRs for `feat-a` and `feat-b` still show the old commits based on stale `main`, and the `feat-c` PR (based on `feat-b`) suddenly shows a1..b2 as "new" commits because their hashes changed. You would have to force-push every branch after fixing them by hand.
2. With `git rebase --update-refs main` git notices that `feat-a` and `feat-b` point at commits that are being rewritten, and moves those refs to the rewritten copies (a2' and b2') at the end. The whole stack ends up as one straight line on top of `m3` with every branch still pointing at "its" top commit, so you just force-push all three (`git push --force-with-lease origin feat-a feat-b feat-c`). In `git rebase -i --update-refs main` the todo list shows them explicitly, e.g. `pick a2 ...` followed by `update-ref refs/heads/feat-a`, then the b commits followed by `update-ref refs/heads/feat-b`. Deleting an `update-ref` line just means that branch is NOT moved -- it stays on the old commit, exactly like the plain rebase. You can also move the line to point a branch at a different commit. (Note: my machine's git was 2.34, and `--update-refs` needs 2.38+, so part 2 is from the docs, not my own run.)
3. `git config --global rebase.updateRefs true` (or per repo without `--global`) makes every rebase behave as if `--update-refs` was given; `--no-update-refs` turns it off for one run. It never moves a branch that is checked out in another worktree (git refuses to rewrite a ref out from under another working tree -- the todo list even notes it), and of course it only updates branches that point at commits in the range being rebased -- a branch pointing at `main` or outside the rebased commits is untouched. It also only touches local `refs/heads/*`, not remote-tracking branches, so you still have to push.
4. Rebase the bottom first, then replay each upper branch with `--onto`, using the OLD tip of the branch below as the upstream so only that branch's own commits move:

   ```bash
   git switch feat-a && git rebase main          # remember old feat-a: ORIG_HEAD / feat-a@{1} / save-a
   git rebase --onto feat-a feat-a@{1} feat-b    # = git rebase --onto <new base> <old base> <branch>
   git rebase --onto feat-b feat-b@{1} feat-c
   ```

   `git rebase --onto NEW OLD BRANCH` takes the commits in `OLD..BRANCH` (here b1,b2 resp. c1) and replays them onto NEW. In my lab I used backup branches `save-a`/`save-b` instead of the reflog syntax and got one straight line `m1 m2 m3 a1 a2 b1 b2 c1`. Forgetting `--onto` and just doing `git rebase feat-a` from `feat-b` usually also works (git skips already-applied patches by patch-id), but it can produce conflicts when the lower commits were edited during the rebase, so `--onto` is the reliable form.
