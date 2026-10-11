# Day 20, Task 7 -- Git: `--first-parent`, `format-patch`/`am`, `revert -m`, `switch --orphan`

## THE TASK

In a SCRATCH repo (`/tmp/fp-lab`, `git init -b main`):

1. Create a `feature` branch with 2 commits, merge it into `main` with `git merge --no-ff`, then add one more commit on `main`. What does `git log --oneline --graph` show, and how does `git log --first-parent` change the picture?
2. Undo the merge with `git revert -m 1 <merge-sha>`. Why is `-m` required, and what does `1` mean?
3. Export the last 2 commits with `git format-patch -2`, then in a second scratch repo apply them with `git am`. What is preserved that `git apply` would lose?
4. What does `git switch --orphan docs` do, and when would you want an orphan branch?
5. After the revert, what happens if you try to merge `feature` again, and how do you get its changes back?

## WHAT I RAN

```
git init -b main /tmp/fp-lab && cd /tmp/fp-lab
echo base > f && git add f && git commit -m base
git switch -c feature
echo 1 > a && git add a && git commit -m f1
echo 2 > b && git add b && git commit -m f2
git switch main
git merge --no-ff feature -m "merge feature"
echo m > m && git add m && git commit -m main3
git log --oneline --graph
git log --oneline --first-parent
git revert -m 1 <merge-sha>
git merge feature
git format-patch -2
# in a second repo: git am 000*.patch
git switch --orphan docs
```

## MY ANSWERS

1. `--graph` shows the branch shape: `main3` on top, then the merge commit, with the two `feature` commits (f2, f1) drawn as a side branch that rejoins at `base`. `git log --first-parent` follows only the first parent of each commit, so it prints `main3`, `merge feature`, `base`. The individual feature commits disappear and the merge appears as one step on main, a clean "what landed on main" history.
2. A merge commit has two parents, so git cannot tell which side of the merge to treat as the mainline to go back to. `-m 1` says to use parent number 1 (the branch you were on when you merged, i.e. `main`) as the mainline, so the revert undoes the changes that came in from parent 2 (`feature`). After the revert, files `a` and `b` are deleted again while `m` stays.
3. `git format-patch -2` writes one mbox-style `.patch` file per commit (`0001-main3.patch`, `0002-...patch`). `git am` applies them and creates real commits, preserving the author, author date and commit message. `git apply` only changes the working tree, so all that metadata is lost and I would have to commit by hand.
4. `git switch --orphan docs` creates a new branch with no parent commit and an empty index/working tree, so it has a completely separate history from `main`. It is useful for content that should not share history with the code, such as a `gh-pages` branch for a static site, or a clean-slate branch for generated docs or a rewrite.
5. `git merge feature` says "Already up to date", because the feature commits are still ancestors of main, and the revert only added a new commit that undid their effect. So the changes do not come back. To get them back, either revert the revert (`git revert <revert-sha>`), or recreate the branch with new commits / rebase `feature` and merge again, e.g. `git cherry-pick` the feature commits.
