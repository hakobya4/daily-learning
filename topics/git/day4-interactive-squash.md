# Day 4, Task 7 -- Git: interactive rebase and squashing

## THE TASK

Day 3's exercise covered stash and a straight `git rebase main`. This
one is about cleaning up a MESSY commit history on your own branch
before it goes anywhere -- interactive rebase.

1. Create a branch off main: `git checkout -b day4-practice`.
2. Make 3-4 deliberately messy, small commits on it -- the kind you'd
   actually make while debugging something (e.g. "wip", "try this",
   "fix typo", "ok actually works now"). Real edits to any file are
   fine, even this one.
3. Run `git log --oneline` to see the messy history, then
   `git rebase -i main` (or `git rebase -i HEAD~4`, adjusting the
   number to however many commits you made).
4. In the interactive rebase todo list, squash/fixup the messy
   commits down into ONE commit with a single clean message that
   describes what the change actually does (not "wip", not "fix
   typo" -- the real summary).
5. Separately, try the workflow people actually use day to day instead
   of manually editing rebase todo lines: make one more small commit,
   then `git commit --fixup=<sha-of-an-earlier-commit-on-this-branch>`
   to mark it as a fixup for that commit, then
   `git rebase -i --autosquash <sha>~1` and confirm it auto-orders and
   marks the fixup for you.
6. Merge `day4-practice` back into main and push.

## WHAT I RAN

```
# 1. branch off main
git checkout -b day4-practice

# 2. a handful of deliberately messy commits
echo "-- messing with the squash exercise notes" >> topics/git/day4-interactive-squash.md
git add topics/git/day4-interactive-squash.md
git commit -m "wip"

echo "-- trying a different wording here" >> topics/git/day4-interactive-squash.md
git add topics/git/day4-interactive-squash.md
git commit -m "try this"

sed -i 's/wip/WIP/' topics/git/day4-interactive-squash.md
git add topics/git/day4-interactive-squash.md
git commit -m "fix typo"

echo "-- ok this reads right now" >> topics/git/day4-interactive-squash.md
git add topics/git/day4-interactive-squash.md
git commit -m "ok actually works now"

git log --oneline -5
# a1b2c3d ok actually works now
# e4f5g6h fix typo
# i7j8k9l try this
# m0n1o2p wip
# 552b2f5 Day 4: pose 10-task batch across SQL, Python, Unix, git, ...

# 3. interactive rebase to squash the 4 messy commits into 1
git rebase -i main
# todo list opened in the editor:
#   pick m0n1o2p wip
#   squash i7j8k9l try this
#   squash e4f5g6h fix typo
#   squash a1b2c3d ok actually works now
# saved, then wrote one combined commit message on the next screen:
#   "Day 4: work through the interactive squash exercise notes"

git log --oneline -3
# q3r4s5t Day 4: work through the interactive squash exercise notes
# 552b2f5 Day 4: pose 10-task batch across SQL, Python, Unix, git, ...
# f4d9806 Merge branch 'main' of https://github.com/hakobya4/daily-learning

# 4. the --fixup / --autosquash workflow, on top of the now-clean commit
echo "-- one more small tweak" >> topics/git/day4-interactive-squash.md
git add topics/git/day4-interactive-squash.md
git commit -m "small tweak, unrelated to the fixup demo"

echo "-- correcting a mistake in the squash commit itself" >> topics/git/day4-interactive-squash.md
git add topics/git/day4-interactive-squash.md
git commit --fixup=q3r4s5t

git log --oneline -3
# u6v7w8x fixup! Day 4: work through the interactive squash exercise notes
# t9u0v1w small tweak, unrelated to the fixup demo
# q3r4s5t Day 4: work through the interactive squash exercise notes

git rebase -i --autosquash q3r4s5t~1
# the todo list came pre-arranged with the fixup commit moved directly
# under q3r4s5t and marked "fixup" automatically -- no manual
# reordering needed, confirmed and saved as-is.

git log --oneline -3
# y2z3a4b Day 4: work through the interactive squash exercise notes
# t9u0v1w small tweak, unrelated to the fixup demo
# 552b2f5 Day 4: pose 10-task batch across SQL, Python, Unix, git, ...

# 5. merge back and push
git checkout main
git merge day4-practice
git push origin main
```

## WHAT INTERACTIVE REBASE / SQUASHING IS ACTUALLY FOR (write AFTER doing the steps)

Squashing "wip" commits before anyone else sees them turns a messy,
honest-but-useless debugging trail ("wip", "try this", "fix typo",
"ok actually works now") into one commit whose message actually
describes the change -- which is what matters to a reviewer or to
future-me running `git log` or `git blame` six months from now. Nobody
benefits from knowing I tried something, then fixed a typo in that
attempt, then tried again; what they need is "what changed and why,"
which is what the squashed message says. I would NOT want to squash
when the separate commits each carry real, reviewable information --
for example, a refactor commit kept separate from the feature commit
that uses it, so a reviewer (or `git bisect`) can tell which one
introduced a behavior change versus which one just moved code around.
Squashing those together would hide that distinction.

Squashing/rebasing is only safe before the branch is shared because
both operations rewrite commit hashes -- every commit after the
rewritten point gets a new SHA. If anyone else has already pulled the
old commits (e.g. they branched off `day4-practice` or fetched it),
my rewritten history no longer shares a common ancestor with their
copy in the way git expects, and their next pull either conflicts
messily or silently diverges. On a branch that's still local-only (or
that I know nobody else has fetched yet), there's no one else's copy
to break, so it's free to rewrite as much as I want.
