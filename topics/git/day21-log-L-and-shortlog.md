# Day 21, Task 7 -- Git: `log -L`, `shortlog`, `cherry`, `merge-base --fork-point`

## THE TASK

In a SCRATCH repo (`/tmp/hist-lab`, `git init -b main`):

1. Create a file with a function in it, change that function in 3 separate commits (and change unrelated lines in 2 others). How do you list only the commits that touched that function's lines, with their diffs? (`git log -L`)
2. Make commits as two different authors (`git -c user.name=... -c user.email=... commit`). Which command summarises commits per author, and what does `-s -n` change?
3. Create `topic` from `main`, cherry-pick one of its commits onto `main`. What does `git cherry -v main topic` print for that commit versus the others, and why does it work without a shared hash?
4. Make `topic`, then rewrite `main` (e.g. `git commit --amend` an old tip after branching). What does `git merge-base --fork-point main topic` find that plain `git merge-base` does not, and which reflog entry does it rely on?
5. How would you attribute each line of a file to the commit that last changed it while ignoring whitespace-only changes and lines moved within the file (`blame` flags)?

## WHAT I RAN

```
(fill in the exact commands you ran)
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
