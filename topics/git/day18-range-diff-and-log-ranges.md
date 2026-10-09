# Day 18, Task 7 -- Git: log ranges, `--first-parent`, `shortlog`, `range-diff`

## THE TASK

In a SCRATCH repo (`/tmp/range-lab`, `git init -b main`):

1. Make 3 commits on `main`, branch `topic` from it, add 3 more commits on `topic`, then merge `topic` into `main` with `git merge --no-ff`.
2. What is the difference between `git log main..topic`, `git log topic..main` and `git log main...topic` (three dots)?
3. What does `git log --first-parent --oneline main` show after the no-ff merge, and why is it useful on a busy main branch?
4. What does `git shortlog -sn` print, and how do you restrict it to one range?
5. Rebase `topic` onto a newer `main` (after adding a commit to `main`). What does `git range-diff main...topic@{1} main...topic` (or the old/new tips) show, and when would you use it?
6. How do you list commits that touched one file with their patches (`git log -p -- <file>`) and follow it through a rename (`--follow`)?

## WHAT I RAN

```
git init -b main /tmp/range-lab && cd /tmp/range-lab
for i in 1 2 3; do echo m$i >> f.txt; git add f.txt; git commit -m "main $i"; done
git switch -c topic
for i in 1 2 3; do echo t$i >> t.txt; git add t.txt; git commit -m "topic $i"; done
git switch main
git merge --no-ff topic -m "Merge topic"
git log main..topic --oneline
git log topic..main --oneline
git log main...topic --oneline
git log --first-parent --oneline main
git shortlog -sn
git shortlog -sn main~1..main
git log -p -- f.txt
git log --follow -p -- renamed.txt
```

## MY ANSWERS

1. Done in the scratch repo: 3 commits on `main`, `topic` branched from it with 3 more commits, then `git merge --no-ff topic` creating a merge commit even though a fast-forward was possible.
2. `git log main..topic` lists commits reachable from `topic` but not from `main` (what topic adds). `git log topic..main` is the reverse: what main has that topic lacks. `git log main...topic` (symmetric difference) lists commits reachable from either one but not both, i.e. everything that diverged. Before the merge, `main..topic` shows the 3 topic commits; after the no-ff merge it is empty, since topic is now reachable from main.
3. `--first-parent` follows only the first parent of each commit, so after a no-ff merge you see the merge commit and main's own direct commits, not the individual commits of the merged branch. On a busy main it gives a clean one-line-per-feature history of what landed and when.
4. `git shortlog -sn` prints commit counts per author (`-s` summary only, `-n` sorted by count, descending). To restrict it, give a range or path: `git shortlog -sn main~10..main` or `git shortlog -sn --since=2.weeks -- src/`.
5. After rebasing `topic` onto a newer `main`, the commit hashes all change. `git range-diff main...topic@{1} main...topic` (or `range-diff old-base..old-tip new-base..new-tip`) pairs old and new commits and shows how each patch changed (unchanged, modified with an inter-diff, added or dropped). Use it to review a rebased or force-pushed branch (for example a PR) and confirm only the intended changes happened, or to compare versions of a patch series.
6. `git log -p -- <file>` lists only commits that touched that file, with their patches. `git log --follow -p -- <file>` keeps tracking the file's history back through a rename (it only works for a single file).
