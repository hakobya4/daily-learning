# Day 25, Task 7 -- Git: `git bundle`, `git stash --keep-index`, `git log --since`, `git shortlog -sn`, `git checkout --orphan`

## THE TASK

In a SCRATCH repo (`/tmp/bundle-lab`, `git init -b main`, a few commits):

1. How do you pack the whole repo (all branches and tags) into a single file you can e-mail (`git bundle create`), and how do you clone from that file? How do you verify it first?
2. What does `git stash push --keep-index` do differently from a plain `git stash`, and when is that useful (e.g. testing only what you staged)?
3. How do you list commits from the last 2 weeks by one author (`--since`, `--author`)? How do you count commits per author (`shortlog -sn`)?
4. What does `git checkout --orphan <name>` (or `git switch --orphan`) create, and what is a legitimate use for it?
5. How do you see which branches are already merged into `main`, and delete only those (`git branch --merged`)?

## WHAT I RAN

```bash
git init -b main /tmp/bundle-lab && cd /tmp/bundle-lab
echo one > a.txt && git add a.txt && git commit -m "one"
git switch -c feature && echo two > b.txt && git add b.txt && git commit -m "two"
git tag v1
git switch main

git bundle create ../lab.bundle --all
git bundle verify ../lab.bundle
git clone ../lab.bundle /tmp/lab-clone

echo three >> a.txt && echo four > c.txt && git add a.txt
git stash push --keep-index

git log --since="2 weeks ago" --author="Narek" --oneline
git shortlog -sn --all

git switch --orphan fresh
git switch main
git branch --merged main
git branch --merged main | grep -v '^\*' | xargs -r git branch -d
```

## MY ANSWERS

1. `git bundle create repo.bundle --all` packs every branch and tag into one file. `git bundle verify repo.bundle` checks it is valid and that its prerequisites are satisfied. Then `git clone repo.bundle my-clone` clones from it like a remote (use `-b <branch>` if HEAD is not usable).
2. A plain `git stash` stashes both staged and unstaged changes and resets the working tree and index. `git stash push --keep-index` stashes everything but leaves the already-staged changes in the index and working tree. It is useful for testing only what you are about to commit: stage the intended hunks, stash the rest, run the tests, commit, then `git stash pop`.
3. `git log --since="2 weeks ago" --author="Name"` lists that author's commits from the last two weeks (add `--oneline` for brevity). `git shortlog -sn` prints commit counts per author, sorted by count (`-s` summary only, `-n` numeric order); add `--all` or `--since` to widen or narrow it.
4. `git checkout --orphan <name>` (or `git switch --orphan <name>`) creates a new branch with no parent commit and no history; the first commit on it is a new root. Legitimate uses: a `gh-pages`/docs branch with unrelated content, or starting a clean history (e.g. publishing code without its private history).
5. `git branch --merged main` lists branches whose tips are already reachable from main. To delete only those: `git branch --merged main | grep -v '^\*' | grep -v main | xargs git branch -d` (lowercase `-d` refuses unmerged branches, so it is safe).
