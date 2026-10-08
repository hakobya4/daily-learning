# Day 17, Task 7 -- Git: resolving a merge conflict, `merge --abort`, and `rerere`

## THE TASK

In a SCRATCH repo (`/tmp/conflict-lab`, `git init -b main`):

1. Commit `app.txt` with three lines on `main`. Create branch `feature`.
2. On `feature` change line 2 to one value; on `main` change line 2 to a
   different value (commit both). Run `git merge feature` on `main`.
3. What do the conflict markers `<<<<<<<`, `=======`, `>>>>>>>` mean, and
   which side is "ours" here?
4. Abort the merge. What state is the repo in afterwards?
5. Enable `git config rerere.enabled true` (local to the scratch repo),
   redo the conflicting merge, resolve it, commit. Then reset back before
   the merge and redo it: what does rerere do differently the second time?
6. How would `git checkout --theirs app.txt` differ from editing by hand?

## WHAT I RAN

```
mkdir /tmp/conflict-lab && cd /tmp/conflict-lab && git init -b main
printf 'one\ntwo\nthree\n' > app.txt && git add . && git commit -m base
git branch feature
git checkout feature && sed -i 's/two/two-feature/' app.txt && git commit -am f
git checkout main && sed -i 's/two/two-main/' app.txt && git commit -am m
git merge feature            # CONFLICT (content): Merge conflict in app.txt
git status -sb               # UU app.txt  (both modified)
git merge --abort
git config rerere.enabled true
git merge feature            # "Recorded preimage for 'app.txt'"
# edit app.txt by hand -> line 2 = two-resolved
git add app.txt && git commit -m merged   # "Recorded resolution for 'app.txt'"
git reset --hard HEAD~1      # back before the merge
git merge feature            # "Resolved 'app.txt' using previous resolution."
git checkout --theirs app.txt
```

## MY ANSWERS

1. Both branches changed line 2 of the same base, so git cannot pick one automatically and stops with a conflict. Branch `feature` has `two-feature`, `main` has `two-main`.
2. Nothing else changed, so git merged the other lines and wrote markers into `app.txt`: `<<<<<<< HEAD` begins our side, `=======` separates the two sides, `>>>>>>> feature` ends their side.
3. Markers: between `<<<<<<<` and `=======` is "ours" (the branch I am on, `main`, i.e. HEAD: `two-main`); between `=======` and `>>>>>>>` is "theirs" (the branch being merged, `feature`: `two-feature`).
4. `git merge --abort` throws away the in-progress merge and restores the pre-merge state: `MERGE_HEAD` is gone, the index and working tree match `main` again, `app.txt` reads `two-main`, and `git status` is clean.
5. With `rerere` ("reuse recorded resolution") enabled, the first conflict records the conflicted preimage, and when I commit the hand-resolution it records my resolution. After resetting and redoing the same merge, git still reports a conflict but says "Resolved 'app.txt' using previous resolution" and fills in `two-resolved` itself. I still have to `git add` and commit, because rerere only edits the working file.
6. `git checkout --theirs app.txt` replaces the whole file with the version from the branch being merged (`two-feature`), throwing away ours for every hunk in that file, with no markers. Editing by hand lets me combine both sides or write a new value on a per-hunk basis. `--theirs` is a blunt all-or-nothing per file (still needs `git add` afterwards).
