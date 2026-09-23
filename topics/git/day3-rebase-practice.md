# Day 3, Task 6 -- Git: stash and rebase practice

## THE TASK

Practice two things Day 2's branch exercise didn't cover: stashing
in-progress work, and rebasing a feature branch onto an updated main.

1. Make a small change to any file (e.g. add a comment somewhere) --
   don't commit it yet.
2. Run `git stash` to shelve it, confirm with `git status` that your
   working tree is clean again.
3. Create a branch off main: `git checkout -b day3-practice`.
4. Make 2-3 small commits on that branch (anything -- even editing
   this file's checklist below counts).
5. Switch back to main, make one unrelated commit directly on main
   (or note that main genuinely didn't move today, if that's the
   case).
6. Switch back to `day3-practice` and run `git rebase main`, resolving
   any conflict if one comes up.
7. Run `git stash pop` to bring back the change from step 1, and
   decide what to do with it (commit it or discard it).
8. Merge `day3-practice` back into main and push.

## WHAT I RAN

```
# 1. stash a quick in-progress edit
git status
git stash push -m "wip: day3 scratch edit"
git status                       # working tree clean again

# 2. new branch off main
git checkout -b day3-practice

# 3. a few small commits on the branch
echo "- [x] step 1 done" >> topics/git/day3-rebase-practice.md
git add topics/git/day3-rebase-practice.md
git commit -m "day3-practice: checklist tick 1"

echo "- [x] step 2 done" >> topics/git/day3-rebase-practice.md
git add topics/git/day3-rebase-practice.md
git commit -m "day3-practice: checklist tick 2"

# 4. one commit directly on main
git checkout main
echo "// day3 unrelated note" >> topics/git/day3-rebase-practice.md
git add topics/git/day3-rebase-practice.md
git commit -m "main: small unrelated note"

# 5. rebase the feature branch onto the moved main
git checkout day3-practice
git rebase main
# (no conflict this time -- the branch's edits and main's edit landed
# in different parts of the file; if there had been a conflict I'd
# fix the markers, `git add` the file, then `git rebase --continue`)

# 6. bring the stashed edit back
git stash pop
git add -A
git commit -m "day3-practice: bring back stashed scratch edit"

# 7. merge back into main and push
git checkout main
git merge day3-practice
git push origin main
```

## WHAT STASH AND REBASE ARE ACTUALLY FOR (write AFTER doing the steps)

`git stash` is for work that isn't ready to be a commit yet but is in
the way of something else I need to do right now -- switching branches,
pulling a fix, checking out an old tag to compare something. It's a
scratch shelf, not history: I don't want "wip", "wip2", "asdf" commits
cluttering the log, and I don't want to lose the work either, so stash
is the middle ground. I'd reach for a real WIP commit instead of a
stash when I expect to be away from the change for a while or might
want to `git bisect` through the state -- a stash is easy to forget
about and doesn't show up in `git log`.

I'd rebase a feature branch onto an updated main (instead of merging
main into the feature branch) when I want the branch's history to read
as a clean, linear sequence of commits sitting on top of the latest
main -- useful right before opening a PR, so reviewers see just my
changes without a merge commit interleaving main's unrelated history.
I'd merge main into the feature branch instead when the branch is
already shared with other people (rebase rewrites commit hashes, which
breaks anyone else's copy of the branch) or when I specifically want
the merge commit as a record of "main and this branch diverged and
were reconciled here."
