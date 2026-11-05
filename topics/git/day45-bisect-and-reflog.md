# Day 45, Task 7 -- Git: bisect and reflog recovery

## THE TASK

In a SCRATCH area (`/tmp/day45-lab`) create a repo with ~8 commits where a
test script (`test.sh`, exits non-zero when broken) passes at first and starts
failing at some middle commit. Then work through the questions.

1. Use `git bisect` to find the first bad commit. Which commands start, mark and end a session? How do you automate it with `git bisect run ./test.sh`?
2. Do a `git reset --hard HEAD~3` and then recover the lost commits using `git reflog`. Which command restores them, and why were the commits not really gone?
3. What is the difference between `git reflog` and `git log`? How long do reflog entries live by default (`gc.reflogExpire`)?
4. After `git bisect reset`, where is HEAD? What does `git bisect skip` do and when would you use it?

## WHAT I RAN

```bash
mkdir -p /tmp/day45-lab && cd /tmp/day45-lab && git init -q
printf '#!/bin/sh\nexit 0\n' > test.sh && chmod +x test.sh
git add . && git commit -qm "c1 good"
for i in 2 3 4; do echo $i > f; git add f; git commit -qm "c$i good"; done
printf '#!/bin/sh\nexit 1\n' > test.sh && git commit -qam "c5 breaks the test"
for i in 6 7 8; do echo $i > f; git add f; git commit -qm "c$i"; done

git bisect start
git bisect bad HEAD
git bisect good HEAD~7
git bisect good        # / git bisect bad, repeated until it names the culprit
git bisect reset

git bisect start HEAD HEAD~7 && git bisect run ./test.sh && git bisect reset

git reset --hard HEAD~3
git reflog
git reset --hard HEAD@{1}      # or the sha shown by reflog
```

## MY ANSWERS

1. `git bisect start`, then `git bisect bad` (current commit is broken) and `git bisect good <rev>` (a known good one). Git checks out the midpoint; I test and mark it `good` or `bad`, repeating in O(log n) steps until it prints "<sha> is the first bad commit". `git bisect reset` ends the session. To automate: `git bisect start <bad> <good>` then `git bisect run ./test.sh`; the script's exit code 0 marks good, 1-127 (except 125) marks bad, and 125 means skip.
2. `git reset --hard HEAD~3` only moves the branch pointer; the three commits remain as objects in the database. `git reflog` lists where HEAD used to point, so I find the old tip (e.g. `HEAD@{1}`) and run `git reset --hard HEAD@{1}` (or `git branch rescue <sha>`) to get them back. They are not gone because nothing deletes unreachable objects until gc prunes them.
3. `git log` walks the commit ancestry reachable from a ref, so after a reset the lost commits vanish from it. `git reflog` is a local, per-repo journal of every movement of HEAD and branch tips (commits, resets, checkouts, rebases), regardless of reachability. It is never pushed. By default entries live 90 days (`gc.reflogExpire`), and 30 days for entries that are unreachable (`gc.reflogExpireUnreachable`).
4. `git bisect reset` checks out the branch/commit I was on before starting (original HEAD), restoring the pre-bisect state. `git bisect skip` tells git to leave out the current commit and pick another when it can't be tested (doesn't build, unrelated breakage); with `bisect run` the script exits 125 for this. If skips hide the culprit, git can only narrow it to a range of candidates.
