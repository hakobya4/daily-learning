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

Scratch repo in /tmp/tag-practice: three commits (f.txt = 1, 2, 3), then

```
git tag v1.0-lw <hash of commit 2>
git tag -a v1.0 -m "First tagged release"

$ git tag
v1.0
v1.0-lw

$ git show v1.0-lw | head -8
commit 3580681cf7f7ad8013ff834fd556e744f724c6fa
Author: Narek <a@b.c>
Date:   Tue Sep 29 03:40:57 2026 +0000

    commit 2

diff --git a/f.txt b/f.txt
index d00491f..0cfbf08 100644

$ git show v1.0 | head -10
tag v1.0
Tagger: Narek <a@b.c>
Date:   Tue Sep 29 03:40:57 2026 +0000

First tagged release

commit c099fb6136bceda76d4fb01bfe3a3ef61806c6e5
Author: Narek <a@b.c>
Date:   Tue Sep 29 03:40:57 2026 +0000


$ git checkout v1.0-lw
Note: switching to 'v1.0-lw'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this

$ git status
HEAD detached at v1.0-lw
nothing to commit, working tree clean

$ git commit  # detached commit 0df422a
$ git checkout main
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  0df422a commit made while detached

If you want to keep it by creating a new branch, this may be a good time
to do so with:


$ git branch rescued-tag-work 0df422a
$ git log --oneline rescued-tag-work
0df422a commit made while detached
3580681 commit 2
b9e23c5 commit 1
```

## LIGHTWEIGHT VS. ANNOTATED -- WHAT'S ACTUALLY DIFFERENT (write AFTER doing the steps)

An annotated tag is a real git object of its own: it stores the tagger's name, a date and a message (`git show v1.0` printed a `tag v1.0 / Tagger / Date / message` block before the commit info), and it can be signed. A lightweight tag is just a named pointer at a commit, so `git show v1.0-lw` went straight to the commit with no tag metadata. Because annotated tags record who tagged a release, when, and why, most projects use them for releases, and `git describe` only considers annotated tags by default. A lightweight tag is still fine as a private, temporary bookmark (e.g. marking a spot locally while debugging) where nobody needs the metadata.

## WHY DETACHED HEAD NEEDS A BRANCH TO SAVE WORK (write AFTER doing the steps)

A commit made in detached HEAD isn't on any branch, so once I checked out `main` nothing pointed at it; git even warned "you are leaving 1 commit behind, not connected to any of your branches". It isn't deleted immediately (it's still in the reflog), but it is unreachable and would eventually be garbage-collected. `git branch rescued-tag-work <hash>` gives it a branch name again, so it is reachable and `git log` shows it. Practical lesson: if you land in detached HEAD (after checking out a tag or an old commit) and want to keep working, run `git switch -c <new-branch>` before or right after committing, so the work always lives on a branch.
