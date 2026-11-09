# Day 48, Task 7 -- Git: merge --no-ff, --squash, --ff-only and rebase --rebase-merges

## THE TASK

In a SCRATCH area (`/tmp/day48-lab`) create a repo and work through the questions by actually running things.

1. Create `main` with 1 commit and a branch `feature` with 2 commits. Merge it with `git merge --no-ff feature`. How does the history graph (`git log --graph --oneline`) differ from a fast-forward merge, and how many parents does the new commit have?
2. Redo it with `git merge --squash feature`. What ends up staged, how many commits did you get, and does git record `feature` as merged (what does `git branch --merged` say afterwards)?
3. What does `git merge --ff-only` do when `main` has diverged, and how do you configure it as the default (`pull.ff`)?
4. What does `git rebase --rebase-merges` preserve that a plain `git rebase` flattens?

## WHAT I RAN

```bash
rm -rf /tmp/day48-lab && git init -q -b main /tmp/day48-lab && cd /tmp/day48-lab
git commit -q --allow-empty -m base
git switch -q -c feature
git commit -q --allow-empty -m f1 && git commit -q --allow-empty -m f2
git switch -q main
git merge --no-ff feature -m "merge feature"      # step 1
git log --graph --oneline
git cat-file -p HEAD | grep -c '^parent'          # 2
# step 2: reset main to base, then
git reset -q --hard HEAD~1 && git merge --squash feature
git status --short && git commit -m "squashed feature"
git branch --merged                               # feature NOT listed
# step 3
git merge --ff-only other-branch                  # refuses when diverged
git config pull.ff only
# step 4
git rebase --rebase-merges main
```

## MY ANSWERS

1. A fast-forward just moves the `main` pointer, leaving a straight line with no trace that a branch existed. `--no-ff` always creates a merge commit, so the graph shows the side branch splitting off and rejoining. That merge commit has 2 parents: the previous `main` tip (first parent) and the `feature` tip (second parent).
2. `--squash` applies the combined changes of `feature` to the index and working tree but does not commit, and it does not create a merge relationship. After I commit I get exactly 1 new ordinary commit with one parent. Git does not record `feature` as merged, so `git branch --merged` does not list it and `git branch -d feature` complains it is not fully merged (needs `-D`).
3. `--ff-only` refuses to merge unless the merge can be a fast-forward. If `main` has diverged it aborts with "fatal: Not possible to fast-forward, aborting." and changes nothing, so I must rebase or do a real merge. Make it the default for pulls with `git config pull.ff only` (add `--global` for all repos).
4. A plain `git rebase` drops merge commits and replays only the non-merge commits, linearizing history. `--rebase-merges` recreates the merge commits, keeping the branch topology (side branches and their merge points) while still replaying the commits on the new base. It is the modern replacement for the old `--preserve-merges`.
