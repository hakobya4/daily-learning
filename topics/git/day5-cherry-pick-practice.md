# Day 5, Task 7 -- Git: cherry-picking a commit across branches

## THE TASK

Days 2-4 covered branching, stashing, a straight `git rebase main`, and
interactive rebase/squash. This one is about `git cherry-pick`: taking
ONE specific commit from one branch and replaying it onto another,
without pulling in everything else that branch has.

1. Create a branch off main: `git checkout -b day5-feature-a`.
2. Make 2 commits on it: one that's a genuinely useful, self-contained
   change (e.g. fixing a typo somewhere, or adding a small note to
   this file), and a second that's unrelated scratch/debug work you
   would NOT want to ship anywhere else.
3. Note the commit hash of the USEFUL commit: `git log --oneline`.
4. Switch back to main and create a second branch:
   `git checkout main && git checkout -b day5-feature-b`.
5. Cherry-pick ONLY the useful commit from `day5-feature-a` onto
   `day5-feature-b`: `git cherry-pick <hash>`. Confirm with
   `git log --oneline` that `day5-feature-b` now has that commit but
   NOT the scratch one.
6. Merge `day5-feature-b` into main and push. Leave `day5-feature-a`
   as-is (don't merge it) -- it still carries the scratch commit you
   deliberately didn't want to bring along.

## WHAT I RAN

I ran this in a scratch git repo to keep the demo self-contained (not
inside this daily-learning repo's own history). Commands, in order:

```
git checkout -b day5-feature-a
echo "Fixed a typo in the readme." >> README.md
git add README.md && git commit -m "Fix typo in README"      # the useful commit
echo "console.log('debug scratch')" > debug.js
git add debug.js && git commit -m "WIP debug scratch, do not ship"

git log --oneline
# 3f6ee3d WIP debug scratch, do not ship
# 404de5d Fix typo in README
# f6ad8e2 Initial commit
# -> useful commit hash: 404de5d

# (main moved on in the meantime with an unrelated "Add changelog"
# commit, so feature-b is NOT a trivial fast-forward of feature-a)

git checkout main
git checkout -b day5-feature-b

git log --oneline                       # BEFORE cherry-pick
# 35e67ee Add changelog
# f6ad8e2 Initial commit

git cherry-pick 404de5d

git log --oneline                       # AFTER cherry-pick
# ba585e5 Fix typo in README
# 35e67ee Add changelog
# f6ad8e2 Initial commit
# -> the cherry-picked commit landed as a NEW hash, ba585e5 (not the
#    original 404de5d), even though its content/message are identical.
#    The scratch "WIP debug" commit never appears on feature-b at all.

git checkout main
git merge day5-feature-b               # fast-forward, then push
```

`day5-feature-a` was left as-is afterward and still carries both of
its original commits (the useful one AND the scratch one) -- only
`day5-feature-b` (and then `main`) got just the useful fix.

## WHAT CHERRY-PICK IS ACTUALLY FOR (write AFTER doing the steps)

Cherry-pick earns its place when you want ONE commit's changes without
the rest of that branch's history coming along -- the two classic
cases are a hotfix that accidentally got committed on the wrong branch
(you cherry-pick just that fix onto the right one instead of merging
everything), and backporting a single bug fix to an older maintenance
release branch without dragging in every newer, unrelated feature that
branch's `main` has picked up since.

The downside showed up directly in the demo above: cherry-pick gives
the replayed commit a brand-new hash (404de5d became ba585e5) even
though the content is identical, because it's a genuinely new commit
object with a different parent. If `day5-feature-a` (which still has
the ORIGINAL 404de5d commit) ever gets merged into `main` later too,
git has no way of knowing "ba585e5 on main" and "404de5d on
feature-a" are the same logical change -- it will try to apply that
diff a second time. Usually git's merge machinery is smart enough to
notice the resulting tree is identical and produces an empty,
conflict-free merge, but if anything nearby has changed in between,
it can turn into a real merge conflict over a change that's already
present -- confusing to untangle precisely because the commit hashes
don't match up. That's the standard argument for keeping cherry-picks
occasional (hotfixes, backports) rather than a routine way to move
work between branches.
