# Day 28, Task 7 -- Git: `reflog expire`, `restore --source`, `branch --contains`, `log --diff-filter`, `stash show -p`

## THE TASK

In a SCRATCH repo (`/tmp/day28-lab`, `git init -b main`, a few commits and a feature branch):

1. How do you restore ONE file to its content from three commits ago without moving HEAD (`git restore --source`)? How does that differ from `git checkout <rev> -- file`?
2. How do you list every branch that contains a given commit (`git branch --contains`)? And every branch NOT yet merged into main (`--no-merged`)?
3. How do you find only the commits that DELETED a file (`git log --diff-filter=D`)?
4. How do you see the full diff of the newest stash without applying it (`git stash show -p`)?
5. What do `git reflog expire --expire=now --all` and `git gc --prune=now` do together, and why is that dangerous?

## WHAT I RAN

```bash
git init -b main /tmp/day28-lab && cd /tmp/day28-lab
for i in 1 2 3 4; do echo "v$i" > f.txt; git add f.txt; git commit -m "c$i"; done
git restore --source=HEAD~3 f.txt          # worktree only, HEAD untouched
git restore --source=HEAD~3 --staged --worktree f.txt
git checkout HEAD~3 -- f.txt               # same content, but also stages it
git switch -c feature && echo x > g.txt && git add g.txt && git commit -m g
git branch --contains HEAD~1
git branch --no-merged main
git rm f.txt && git commit -m "delete f"
git log --diff-filter=D --oneline -- f.txt
echo wip >> g.txt && git stash
git stash show -p stash@{0}
git reflog expire --expire=now --all && git gc --prune=now
```

## MY ANSWERS

1. `git restore --source=HEAD~3 file` copies the file's content from that commit into the working tree (add `--staged` to also update the index) and never moves HEAD or the branch. `git checkout HEAD~3 -- file` gives the same content but always writes to both index and working tree; `restore` is the newer, clearer command, whose default target is only the working tree.
2. `git branch --contains <commit>` lists branches whose history includes the commit; `git branch --no-merged main` lists branches with commits not yet reachable from main.
3. `git log --diff-filter=D --oneline -- <path>` shows only commits where the file was deleted (D = deleted; A, M, R work similarly).
4. `git stash show -p` (optionally `stash@{n}`) prints the full patch of the newest stash without applying or dropping it; without `-p` you only get a stat summary.
5. `reflog expire --expire=now --all` throws away every reflog entry, so commits that are only reachable via the reflog (old HEADs after reset/rebase, dropped stashes' work) become unreachable; `gc --prune=now` then physically deletes those unreachable objects immediately. Together they make accidental loss permanent, with no safety net to recover from.
