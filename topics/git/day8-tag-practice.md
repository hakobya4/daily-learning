# Day 8, Task 8 -- Git: lightweight vs. annotated tags, and detached HEAD

## THE TASK

Days 2-7 covered branching/stashing, rebase (straight and interactive/
squash), cherry-pick, bisect, and reflog. This one is about `git tag`
-- marking a specific commit as a release point -- and what happens
when you check one out.

1. In a SCRATCH repo (not this daily-learning repo's own history):
   `mkdir /tmp/tag-practice && cd /tmp/tag-practice && git init`.
2. Make 3 small commits on top of each other (any tiny file changes).
3. On the SECOND commit, create a LIGHTWEIGHT tag:
   `git tag v1.0-lw <second-commit-hash>` (lightweight tags just take a
   name and a commit, no `-a`/`-m`).
4. On the current HEAD (the third commit), create an ANNOTATED tag:
   `git tag -a v1.0 -m "First tagged release"`.
5. Run `git tag` to list both, then compare `git show v1.0-lw` against
   `git show v1.0` -- one of them shows real tag metadata (tagger name,
   date, message) before the commit info; the other doesn't, because
   it's really just a named pointer straight at the commit.
6. `git checkout v1.0-lw` and run `git status`. Read the message git
   prints carefully -- you're now in "detached HEAD" state, not on any
   branch.
7. While still detached, make ONE new commit (any tiny change). Note
   its hash, then run `git checkout main` (or `master`, whatever your
   default branch is called) to leave detached HEAD -- git will warn
   you this commit isn't on any branch.
8. Recover that "stranded" commit the way Day 7's reflog task taught
   you: `git branch rescued-tag-work <that-commit-hash>`, then confirm
   with `git log --oneline rescued-tag-work` that it's there.

## WHAT I RAN

TODO: paste the actual commands you ran, in order -- the 3 initial
commits, both tag commands, the `git show` output for each tag (enough
of it to show the difference), the detached-HEAD warning from
`git status`, the commit you made while detached, and the
`git branch rescued-tag-work ...` recovery plus its confirmation.

## LIGHTWEIGHT VS. ANNOTATED -- WHAT'S ACTUALLY DIFFERENT (write AFTER doing the steps)

TODO: a few sentences. What extra information does an annotated tag
actually store that a lightweight one doesn't (think about what
`git show` printed for each)? Given that difference, why do most
real-world projects (and tools like `git describe`) prefer annotated
tags for actual releases, and when (if ever) would a lightweight tag
still be a reasonable choice?

## WHY DETACHED HEAD NEEDS A BRANCH TO SAVE WORK (write AFTER doing the steps)

TODO: a few sentences. Based on step 7-8: if you commit while in
detached HEAD and then just check out a branch without doing anything
else first, what happens to that commit from git's point of view, and
why does creating a new branch pointing at its hash (like Day 7's
reflog recovery) fix that? What's the practical lesson for anyone who
ends up in detached HEAD by accident (e.g. from checking out a tag or
an old commit directly) and wants to keep working from there?
