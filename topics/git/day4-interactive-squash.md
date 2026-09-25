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

TODO: paste the actual commands you ran, in order (including the
`git log --oneline` output before AND after the rebase, so the
before/after is visible) -- not the list above, your real terminal
history.

## WHAT INTERACTIVE REBASE / SQUASHING IS ACTUALLY FOR (write AFTER doing the steps)

TODO: a few sentences -- why squash "wip" commits before they're
visible to anyone else, instead of just leaving them in history? When
would you NOT want to squash (i.e., when do separate commits carry
real information worth keeping)? And same caution as Day 3's rebase
note -- why is squashing/rebasing a branch only safe before it's
shared with anyone else?
