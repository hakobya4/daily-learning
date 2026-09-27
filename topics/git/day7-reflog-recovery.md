# Day 7, Task 7 -- Git: recovering a "lost" commit with `git reflog`

## THE TASK

Days 2-6 covered branching/stashing, straight rebase, interactive
rebase/squash, cherry-pick, and bisect. This one is about
`git reflog`: recovering a commit that looks "gone" after something
like `git reset --hard` moves a branch pointer away from it. A plain
`git log` from the new position won't show that commit anymore
(it's no longer an ancestor of HEAD) -- but reflog keeps its own
record of everywhere HEAD and your branch tips have pointed recently,
independent of the commit graph itself.

1. In a SCRATCH repo (not this daily-learning repo's own history):
   `mkdir /tmp/reflog-practice && cd /tmp/reflog-practice && git init`.
2. Make 3-4 small commits on top of each other (any tiny file changes).
3. Note the hash of your LAST commit (`git log --oneline -1`), then
   run `git reset --hard HEAD~2` to make it look like the last two
   commits vanished. Confirm with `git log --oneline` that they're no
   longer visible.
4. Run `git reflog` and find the entry for the commit you just
   "lost" (it'll still be right there, with its full hash).
5. Recover it TWO different ways, and notice what each one actually
   does differently:
   - `git reset --hard <lost-commit-hash>` -- moves your CURRENT
     branch pointer straight back to it.
   - `git branch recovered-work <lost-commit-hash>` -- creates a
     BRAND NEW branch pointing at it, leaving your current branch
     exactly where the reset left it.
6. Confirm the recovered commit's content is actually back, with
   `git show <hash>` or `git log`, for whichever recovery you used.

## WHAT I RAN

TODO: paste the actual commands you ran, in order -- the commits
before the reset, the `git reset --hard` that "lost" them, the
`git reflog` output showing the lost commit's own entry, and the
recovery command you used with confirmation the content came back.

## WHY REFLOG ISN'T A PERMANENT SAFETY NET (write AFTER doing the steps)

TODO: a few sentences. Reflog entries expire after a while (they're
not kept forever), and they live ONLY in your own local `.git`
directory -- they're never pushed, fetched, or cloned anywhere else.
Given that, what's actually true (and what's actually FALSE) about
calling reflog a "safety net" for something like `git reset --hard`?
Name one situation it genuinely protects you in, and one situation
(think about a different machine, or a long-abandoned branch) it
explicitly does NOT protect you in.
