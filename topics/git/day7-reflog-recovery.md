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

Setup -- 4 tiny commits, each appending one line to `file.txt`:

```
$ git init
$ git commit -m "commit 1: add file.txt"      # file.txt: line1
$ git commit -m "commit 2: append line2"      # file.txt: line1, line2
$ git commit -m "commit 3: append line3"      # file.txt: line1, line2, line3
$ git commit -m "commit 4: append line4"      # file.txt: line1, line2, line3, line4

$ git log --oneline
c403d1a commit 4: append line4
da9461d commit 3: append line3
da8b631 commit 2: append line2
8e46ede commit 1: add file.txt
```

Losing the last two commits with `git reset --hard HEAD~2`:

```
$ git reset --hard HEAD~2
HEAD is now at da8b631 commit 2: append line2

$ git log --oneline
da8b631 commit 2: append line2
8e46ede commit 1: add file.txt
```

Commits 3 and 4 (`da9461d`, `c403d1a`) are no longer reachable from
`git log`. `git reflog` still has them, though:

```
$ git reflog
da8b631 HEAD@{0}: reset: moving to HEAD~2
c403d1a HEAD@{1}: commit: commit 4: append line4
da9461d HEAD@{2}: commit: commit 3: append line3
da8b631 HEAD@{3}: commit: commit 2: append line2
8e46ede HEAD@{4}: commit (initial): commit 1: add file.txt
```

`c403d1a` (the "lost" commit 4, which also carries commit 3 as its
parent) is right there in `HEAD@{1}`.

**Recovery, way 1 -- `git reset --hard <hash>`** (moves the current
branch pointer straight back):

```
$ git reset --hard c403d1a
HEAD is now at c403d1a commit 4: append line4

$ git log --oneline
c403d1a commit 4: append line4
da9461d commit 3: append line3
da8b631 commit 2: append line2
8e46ede commit 1: add file.txt

$ cat file.txt
line1
line2
line3
line4
```

Content confirmed back -- both commits 3 and 4 are visible again in
`git log`, and `file.txt` has all four lines.

**Recovery, way 2 -- `git branch <newname> <hash>`** (after redoing
the same "lose the commits" reset, to demo this on a clean slate):

```
$ git reset --hard HEAD~2
HEAD is now at da8b631 commit 2: append line2

$ git branch recovered-work c403d1a

$ git log --oneline                  # current branch (master): UNCHANGED
da8b631 commit 2: append line2
8e46ede commit 1: add file.txt

$ git log --oneline recovered-work   # new branch: has the "lost" commits
c403d1a commit 4: append line4
da9461d commit 3: append line3
da8b631 commit 2: append line2
8e46ede commit 1: add file.txt

$ git show recovered-work:file.txt
line1
line2
line3
line4

$ git branch
* master
  recovered-work
```

The difference is exactly what the task description predicted: way 1
overwrote where `master` was pointing (its history now includes
commits 3 and 4 again); way 2 left `master` exactly at commit 2 and
instead created a second branch, `recovered-work`, pointing at the
recovered commit, so both the "reset" state and the "recovered" state
exist side by side as two separate branches.

## WHY REFLOG ISN'T A PERMANENT SAFETY NET (write AFTER doing the steps)

Reflog is a *local, time-limited* safety net, not a permanent or
shared one, and both halves of that matter.

Local: the reflog lives only inside your own repo's `.git` directory
(specifically `.git/logs/`). It is never part of what gets pushed,
fetched, or cloned -- a teammate cloning your repo, or you cloning it
fresh onto a different machine, gets none of your reflog history.
So reflog absolutely does NOT protect you from something like force-
pushing over a branch on a shared remote and then losing your local
clone, or from a colleague's `git reset --hard` on their own machine
-- their local reflog is theirs alone, and yours (on a different
checkout) never had those entries to begin with.

Time-limited: reflog entries expire. By default, unreachable commits
referenced only by reflog entries get garbage-collected after about
30 days (`gc.pruneExpire`), and reachable ones' reflog entries expire
after about 90 days (`gc.reflogExpire`) -- and `git gc` can run
automatically in the background well before you'd think to look. So
reflog protects you well against "I made a mistake five minutes (or
even a few weeks) ago, on this same machine, in this same repo" -- but
it explicitly does NOT protect you against recovering something from
a long-abandoned branch you deleted six months ago on this machine, or
against anything that only ever existed on a machine you no longer
have (a laptop that got wiped, a CI runner, etc.). In both of those
cases, once the commit is unreachable AND its reflog entry has
expired AND gc has actually run, the object data itself is genuinely
gone -- reflog can't reach back further than its own retention window,
and it was never a backup that traveled with the repo in the first
place.
