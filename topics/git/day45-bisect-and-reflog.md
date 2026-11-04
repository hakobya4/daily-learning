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
# TODO: paste the commands you actually ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
