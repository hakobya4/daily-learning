# Day 57, Task 8 -- Git: revision syntax (`~` vs `^`, `@{u}`, `:/text`, `^{tree}`) and ahead/behind counts

## THE TASK

In a SCRATCH repo (`/tmp/day57-lab`, `git init`) make a history with at least one MERGE commit whose second parent is a side branch of 2-3 commits, and a local branch that tracks a second scratch repo used as its "remote" (`git clone /tmp/day57-lab /tmp/day57-clone`, then commit on both sides so the clone's branch is both ahead of AND behind `origin/main`). Then answer the questions by actually running the commands -- never in a real project's history.

1. On the merge commit `M`: what do `M^`, `M^1`, `M^2`, `M~1`, `M~2`, `M^2~1` and `M^^2` each resolve to? Draw the graph (ASCII is fine) and label every commit you reached. Why is `M^2` != `M~2`? Check each one with `git rev-parse --short`.
2. Use `git rev-parse` to print: the full hash of `HEAD`, the TREE object of `HEAD` (`HEAD^{tree}`), the blob of a file as it was two commits ago (`HEAD~2:path/to/file`), and the most recent commit whose message matches a word (`:/word`). What does `git cat-file -t` say for each? What does `HEAD^{commit}` do on a TAG name (try it on an annotated tag)?
3. In the clone: what do `@`, `@{u}` (`@{upstream}`), `@{push}`, `@{1}` and `main@{yesterday}` (or `@{2.minutes.ago}`) refer to? Which of them come from the REFLOG and are therefore local-only and not shared with anyone?
4. Print how many commits the clone's branch is ahead and behind its upstream with ONE command (`git rev-list --left-right --count @{u}...HEAD`), and explain which number is which and why the THREE-dot range is required here. Then list the actual commits on each side with `git log --oneline --left-right --cherry-mark @{u}...HEAD` and explain the `<`, `>` and `=` markers (make one commit a cherry-pick of the other side's commit so a `=` shows up).

## WHAT I RAN

```bash
# TODO: fill in the exact commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
