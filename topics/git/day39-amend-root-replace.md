# Day 39, Task 7 -- Git: amend, rebase --root and replace

## THE TASK

In a SCRATCH area (`/tmp/day39-lab`) create a repo with 3 commits (`A`, `B`, `C`) on `main`, then practice rewriting history.

1. Your latest commit has the wrong author and message. Which single command fixes both the message and resets the author/date to the current config? What changes about the commit (hash? parents? tree?) and why?
2. The mistake is in the very FIRST commit `A` (e.g. a wrong file was committed). Plain `git rebase -i HEAD~N` cannot reach it. Which flag lets you edit the root commit, and what do you mark in the todo list?
3. What does `git commit --amend --no-edit` do versus `git commit --amend -a`? When is `--no-edit` useful?
4. `git replace <old> <new>` lets you swap one commit for another WITHOUT rewriting history. How does it work, how do you see active replacements, and how do you make a replacement permanent (hint: `git replace --graft` / `filter-repo` idea)?
5. After rewriting published history, why must you use `git push --force-with-lease` and not plain `--force`?

## WHAT I RAN

```bash
# TODO: paste the commands you actually ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
