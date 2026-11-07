# Day 47, Task 7 -- Git: gc, prune, fsck and unreachable objects

## THE TASK

In a SCRATCH area (`/tmp/day47-lab`) create a repo and work through the questions by actually running things.

1. Make 3 commits, then `git reset --hard HEAD~1`. Is the dropped commit gone? Which command lists it (`git fsck --lost-found` / `--unreachable`) and which keeps it reachable (hint: reflog)?
2. Expire the reflog (`git reflog expire --expire=now --all`) and run `git gc --prune=now`. What happens to the dropped commit and why would a plain `git gc` not remove it right away (hint: `gc.pruneExpire`)?
3. What is the difference between `git gc`, `git prune` and `git repack -ad`? What does a packfile buy you over loose objects?
4. What does `git fsck` report for a dangling blob vs a dangling commit, and how can you recover a dangling commit by hash?

## WHAT I RAN

```bash
cd /tmp/day47-lab && git init
for i in 1 2 3; do echo $i > f; git add f; git commit -m "c$i"; done
D=$(git rev-parse HEAD)            # remember the commit that will be dropped
git reset --hard HEAD~1            # drop it from the branch
git reflog                         # still lists $D as HEAD@{1}
git fsck --unreachable --no-reflogs   # reports: unreachable commit $D
git reflog expire --expire=now --all
git gc --prune=now
git cat-file -t $D                 # fatal: Not a valid object name -> gone
```

## MY ANSWERS

1. No, it is not gone. `reset --hard` only moves the branch pointer; the commit object stays in the object database and the reflog (`git reflog`, `HEAD@{1}`) still points at it, so it stays reachable through the reflog. `git fsck --unreachable --no-reflogs` (or `--lost-found`) lists it once reflogs are ignored.
2. After the reflog is expired nothing references the commit, and `gc --prune=now` deletes the unreachable object for good (`git cat-file -t` fails). A plain `git gc` keeps unreachable objects younger than `gc.pruneExpire` (default 2 weeks) as a safety net against races with concurrent commands and to allow recovery; reflog entries also expire by default (90 days reachable, 30 days unreachable).
3. `git gc` is the housekeeping wrapper: it packs refs, repacks loose objects, expires reflogs and prunes old unreachable objects. `git prune` only deletes unreachable loose objects (older than the expiry). `git repack -ad` packs all reachable objects into one pack (`-a` all, `-d` delete redundant packs) but does not expire reflogs. A packfile stores objects delta-compressed against each other in one file with an index, so the repo is far smaller, faster to transfer and read, and uses far fewer inodes than thousands of loose zlib files.
4. `git fsck` prints `dangling blob <sha>` for an unreferenced file content (e.g. a staged-then-reset file) and `dangling commit <sha>` for a commit nothing points to. Recover a dangling commit by hash: inspect with `git show <sha>`, then `git branch rescued <sha>` (or `git cherry-pick <sha>` / `git merge <sha>`). A dangling blob is recovered with `git cat-file -p <sha> > file`. This only works before prune removes the object.
