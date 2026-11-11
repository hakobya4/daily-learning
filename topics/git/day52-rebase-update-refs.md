# Day 52, Task 8 -- Git: stacked branches and `git rebase --update-refs`

## THE TASK

In a SCRATCH area (`/tmp/day52-lab`) create a repo with a few commits on `main`, then build a "stack" of branches: `feat-a` (2 commits) off `main`, `feat-b` (2 commits) off `feat-a`, and `feat-c` (1 commit) off `feat-b`. Add one more commit to `main`. Work through the questions by actually running things.

1. Check out `feat-c` and run a plain `git rebase main`. Where do `feat-a` and `feat-b` point afterwards (`git log --oneline --graph --all`)? Why is that a problem for stacked pull requests?
2. Reset the lab (or rebuild it) and repeat with `git rebase --update-refs main`. What happens to `feat-a` and `feat-b` now? What do the `update-ref` lines look like in `git rebase -i --update-refs main`'s todo list, and what happens if you delete one?
3. How do you make this the default (`rebase.updateRefs`)? Which branches does it NOT update (hint: a branch checked out in another worktree)?
4. Before `--update-refs` existed, how would you have fixed the stack by hand (e.g. `git rebase --onto`)? Write the exact commands for `feat-b` and `feat-c` after `feat-a` was rebased.

## WHAT I RAN

```bash
# TODO: fill in the exact commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
