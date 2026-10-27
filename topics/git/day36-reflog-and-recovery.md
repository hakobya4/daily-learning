# Day 36, Task 7 -- Git: reflog and recovering lost commits

## THE TASK

In a SCRATCH repo (`/tmp/day36-lab`, `git init -b main`): make 3 commits, then run `git reset --hard HEAD~2` and later recover the lost commits.

1. What is the reflog, how does it differ from `git log`, and how long do entries live by default?
2. After `git reset --hard HEAD~2`, how do you find the SHA of the commit you lost, and how do you get back to it (two ways)?
3. What does `HEAD@{1}` mean vs `HEAD~1`? What does `main@{yesterday}` do?
4. You deleted a branch with `git branch -D topic`. How do you bring it back?
5. What do `git fsck --lost-found` and `git gc --prune=now` have to do with unreachable commits?

## WHAT I RAN

```bash
rm -rf /tmp/day36-lab && mkdir /tmp/day36-lab && cd /tmp/day36-lab
git init -b main
for i in 1 2 3; do echo $i > f.txt; git add f.txt; git commit -m "c$i"; done
git log --oneline            # c3 c2 c1
git reset --hard HEAD~2      # main now at c1; c2, c3 look "lost"
git reflog                   # shows HEAD@{1} = c3 with its SHA
git reset --hard HEAD@{1}    # way 1: move main back to c3
# way 2 (non-destructive): git branch rescue <sha>   or   git cherry-pick <sha>
git checkout -b topic && git checkout main && git branch -D topic
git reflog                   # find last commit of topic
git branch topic <sha>       # restore deleted branch
git fsck --lost-found        # lists dangling commits
```

## MY ANSWERS

1. The reflog is a local, per-ref journal of where HEAD and each branch tip pointed over time (every commit, checkout, reset, rebase, merge). `git log` walks the commit graph reachable from a ref; the reflog records movement and so also shows commits no longer reachable. It is not pushed or shared. Entries expire after 90 days by default (`gc.reflogExpire`), 30 days for unreachable ones (`gc.reflogExpireUnreachable`).
2. Run `git reflog` (or `git log -g`) and find the entry from before the reset, e.g. `HEAD@{1}` with its SHA. Way one: `git reset --hard <sha>` (or `HEAD@{1}`) to move the branch back. Way two: leave the branch alone and `git branch rescue <sha>` / `git cherry-pick <sha>` / `git merge <sha>` to bring the commits back.
3. `HEAD@{1}` is where HEAD was one move ago (reflog position, can be on another branch); `HEAD~1` is the first parent of the current commit (graph position). `main@{yesterday}` is where local `main` pointed yesterday, according to the reflog.
4. `git reflog` to find the SHA of the branch's last commit (the checkout/commit entries), then `git branch topic <sha>` (or `git checkout -b topic <sha>`). `git branch -D` prints the abbreviated SHA when it deletes, which also works.
5. Unreachable commits aren't deleted immediately; they stay in the object store. `git fsck --lost-found` finds dangling objects and writes them into `.git/lost-found/`, handy when the reflog entry is gone. `git gc --prune=now` permanently deletes unreachable objects (after expiring reflogs, otherwise reflog entries keep them reachable), so recovery is no longer possible afterward.
