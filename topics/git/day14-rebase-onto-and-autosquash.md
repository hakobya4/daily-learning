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

```
rm -rf /tmp/onto-lab && mkdir /tmp/onto-lab && cd /tmp/onto-lab
git init -b main
echo base > a.txt && git add a.txt && git commit -m "base"
git switch -c topic
echo "t1 line wiht typo" > topic.txt && git add topic.txt && git commit -m t1
echo t2 >> topic.txt && git commit -am t2
echo t3 >> topic.txt && git commit -am t3
# fix the typo in the t1 line, then record it as a fixup of t1
sed -i 's/wiht/with/' topic.txt
git commit -a --fixup <sha-of-t1>
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash main
git log --oneline
git switch -c feature
echo f1 > f.txt && git add f.txt && git commit -m f1
git branch feature-old feature          # keep a copy for range-diff
git rebase --onto main topic feature
git range-diff main feature-old feature
```

## WHAT EACH COMMAND SHOWED (write AFTER)

- The fixup commit's message is `fixup! t1` (the subject of the target
  commit prefixed with `fixup!`). With `--autosquash`, the todo list is
  reordered so that the `fixup!` commit sits directly after `t1` and its
  action is changed from `pick` to `fixup`, so it is melted into t1 and
  its message is discarded. `git log --oneline` then shows main's base
  plus just t1, t2, t3 (three commits, no fixup entry) with new hashes
  for t1 and everything after it. t1 now contains the corrected line.
- `rebase --onto main topic feature` took only the commits reachable from
  `feature` but NOT from `topic` (that is just `f1`) and replayed them on
  top of `main`. The topic commits t1-t3 were left behind: `feature` no
  longer contains them. The old `feature` commits stay reachable through
  the reflog / my `feature-old` copy.
- `git range-diff main feature-old feature` pairs the old and new commits
  and reports f1 as unchanged in message but with a changed diff context
  (or `=` if it applied identically); the t1-t3 commits appear as only
  in the old range, i.e. they were dropped.

## WHEN I WOULD USE EACH (write in your own words)

`commit --fixup` plus `rebase --autosquash` is for small corrections to
a commit that is already made but not yet pushed or reviewed: I record
the fix right away while it is fresh, and tidy history in one go
later instead of fiddling in an interactive editor.

`rebase --onto newbase upstream branch` means: take the commits of
`branch` that are not in `upstream` and replay them onto `newbase`.
I use it when a branch was started from the wrong base (for example
from another unfinished topic branch) or when I want to cut out a
middle section of history. The three arguments are the new place to
land (newbase), the old boundary that says which commits to skip
(upstream), and the branch whose own commits are moved (branch).

`git range-diff` compares two versions of a series of commits. It is
useful after a rebase or amend, or when a reviewer asks "what changed
since v1?" of a patch series, because it shows per-commit what changed
rather than one big diff.
