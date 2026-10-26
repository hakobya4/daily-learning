# Day 35, Task 7 -- Git: merge-base, two-dot vs three-dot diff

## THE TASK

In a SCRATCH repo (`/tmp/day35-lab`, `git init -b main`): make 2 commits on `main`, branch `feature` from the second, add 2 commits on `feature`, then add 1 more commit on `main`.

1. What does `git merge-base main feature` print, and why is it the "fork point"? How does `git merge-base --is-ancestor A B` report its answer?
2. What is the difference between `git diff main feature` (two-dot) and `git diff main...feature` (three-dot)? Which one shows only what `feature` changed since the fork?
3. How do `git log main..feature`, `git log feature..main` and `git log main...feature` differ? What does `--left-right` add?
4. How would you list the files changed on `feature` only (`--name-only`) and the summary of changes (`--stat`)?
5. What does `git merge-base --fork-point main` do differently from plain `merge-base`, and when does it matter (hint: reflog / rebased upstream)?

## WHAT I RAN

```bash
rm -rf /tmp/day35-lab && mkdir /tmp/day35-lab && cd /tmp/day35-lab
git init -b main
echo 1 > a.txt && git add a.txt && git commit -m "m1"
echo 2 >> a.txt && git commit -am "m2"
git switch -c feature
echo f1 > f.txt && git add f.txt && git commit -m "f1"
echo f2 >> f.txt && git commit -am "f2"
git switch main
echo 3 >> a.txt && git commit -am "m3"

git merge-base main feature
git merge-base --is-ancestor main feature; echo $?
git diff main feature
git diff main...feature
git log --oneline main..feature
git log --oneline feature..main
git log --oneline --left-right main...feature
git diff --name-only main...feature
git diff --stat main...feature
git merge-base --fork-point main feature
```

## MY ANSWERS

1. `git merge-base main feature` prints the hash of the best common ancestor: here commit m2, the last commit both branches share, which is where `feature` was created (the fork point). `git merge-base --is-ancestor A B` prints nothing; it reports through the exit code: 0 if A is an ancestor of B, 1 if not (other values on error).
2. `git diff main feature` (two-dot) compares the two tips directly, so it includes the change made on `main` after the fork (m3) shown in reverse, plus what `feature` added. `git diff main...feature` (three-dot) compares the merge-base with `feature`, so it shows only what `feature` changed since the fork.
3. `git log main..feature` lists commits reachable from `feature` but not `main` (f1, f2). `git log feature..main` is the reverse (m3). `git log main...feature` (symmetric difference) lists commits reachable from either one but not both (m3, f1, f2). `--left-right` prefixes each commit with `<` (left side, main) or `>` (right side, feature) so you can tell which side it came from.
4. `git diff --name-only main...feature` lists just the changed file names on `feature` since the fork; `git diff --stat main...feature` gives the per-file summary with insertions/deletions counts.
5. `--fork-point` also consults the reflog of the given ref (e.g. `main`/`origin/main`) to find where your branch actually forked from earlier positions of that ref, not just its current history. It matters when the upstream branch was rebased or force-pushed: plain `merge-base` would use the rewritten history and may pick a too-old ancestor, while `--fork-point` finds the original base so `git rebase` doesn't replay commits that were already upstream.
