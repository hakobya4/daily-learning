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

TODO: paste the actual commands you ran, in order, including the
`git log --oneline` output on `day5-feature-b` BEFORE and AFTER the
cherry-pick so the effect is visible.

## WHAT CHERRY-PICK IS ACTUALLY FOR (write AFTER doing the steps)

TODO: a few sentences -- when would you reach for cherry-pick instead
of merging or rebasing a whole branch? (Hint: think about a hotfix
that got committed on the wrong branch, or backporting a single fix to
an older release branch without dragging in newer unrelated work.)
What's the downside of cherry-picking often instead of properly
merging/rebasing -- it creates a brand-new commit with a NEW hash, so
what could that cause later if the original commit's branch eventually
gets merged too?
