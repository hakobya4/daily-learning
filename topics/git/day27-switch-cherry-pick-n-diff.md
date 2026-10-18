# Day 27, Task 7 -- Git: `git switch`, `cherry-pick -n`, `diff --stat/--name-status`, `log --since`, aliases

## THE TASK

In a SCRATCH repo (`/tmp/day27-lab`, `git init -b main`, a few commits on two branches):

1. How do you create and switch to a new branch with `git switch`, and how does that differ from `git checkout -b`? What does `git switch -` do?
2. How do you apply the changes of one commit from another branch WITHOUT committing them (`cherry-pick -n`)? When is that useful?
3. How do you see a summary of changes between two branches (`git diff --stat`) and just the names with status letters (`--name-status`)?
4. How do you list only commits from the last 2 weeks by one author (`git log --since`, `--author`)?
5. How do you create a shortcut such as `git lg` for a pretty one-line graph log (`git config alias`)? Where is it stored?

## WHAT I RAN

```bash
rm -rf /tmp/day27-lab && mkdir /tmp/day27-lab && cd /tmp/day27-lab
git init -b main
echo one > a.txt && git add a.txt && git commit -m "add a"
git switch -c feature
echo two > b.txt && git add b.txt && git commit -m "add b"
echo three >> a.txt && git commit -am "edit a"
git switch -            # back to main
git cherry-pick -n feature~1   # apply "add b" to the working tree/index only
git status --short
git commit -m "bring b over"
git diff --stat main feature
git diff --name-status main feature
git log --since="2 weeks ago" --author="Narek" --oneline
git config --global alias.lg "log --oneline --graph --decorate --all"
git lg
```

## MY ANSWERS

1. `git switch -c name` creates and switches to a branch (same as `git checkout -b name`). `switch` only handles branches, while `checkout` also restores files, so `switch` is less error-prone. `git switch -` jumps back to the previously checked-out branch.
2. `git cherry-pick -n <commit>` (`--no-commit`) applies that commit's changes to the working tree and index without creating a commit. Useful to combine several commits into one, tweak the change first, or take only part of a commit.
3. `git diff --stat main feature` shows files changed with insertion/deletion counts per file. `git diff --name-status main feature` lists only file names with a status letter: A added, M modified, D deleted, R renamed.
4. `git log --since="2 weeks ago" --author="name"` lists only commits from the last two weeks by that author; add `--oneline` for compact output.
5. `git config --global alias.lg "log --oneline --graph --decorate --all"` then run `git lg`. Global aliases are stored in `~/.gitconfig` under `[alias]`; without `--global` they go in the repo's `.git/config`.
