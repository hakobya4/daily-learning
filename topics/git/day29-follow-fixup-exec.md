# Day 29, Task 7 -- Git: `log --follow`, `blame -w -C`, `commit --fixup`, `rebase --exec`, `includeIf`

## THE TASK

In a SCRATCH repo (`/tmp/day29-lab`, `git init -b main`, a few commits):

1. A file was renamed (`git mv old.txt new.txt`). How do you see its history ACROSS the rename (`git log --follow`)? Why does plain `git log -- new.txt` stop at the rename?
2. What do `git blame -w` and `git blame -C` ignore/detect, and when is each useful (re-indented code, code moved between files)?
3. How do you create a commit that is meant to be squashed into an earlier commit (`git commit --fixup=<rev>`), and how does `git rebase -i --autosquash` use it?
4. How do you run the test command after EVERY commit of a branch during a rebase (`git rebase --exec`), and what happens when one fails?
5. How can you use a different `user.email` for repos under `~/work/` only (`includeIf "gitdir:..."` in `~/.gitconfig`)? How do you verify which value wins (`git config --show-origin --get user.email`)?

## WHAT I RAN

```bash
(fill in the exact commands you ran, in order)
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
