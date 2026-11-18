# Day 59, Task 8 -- Git: dry-run merges with `merge-tree --write-tree`, conflict styles (`merge` / `diff3` / `zdiff3`), and `--ancestry-path`

## THE TASK

In a SCRATCH repo (`/tmp/day59-lab`, `git init -b main`) create a file `config.txt` with ~10 lines and commit it. Branch `left` and `right` off that commit; on each, change the SAME line differently (a real conflict) and on `right` also change a line far away (a clean change). Add one more commit on `main` that touches a different file. Then answer the questions by actually running the commands -- never in a real project's history.

1. Without touching the working tree or index, ask git whether `left` and `right` would merge cleanly: `git merge-tree --write-tree left right`. What does it print on stdout (the first line, the "Conflicted file info" section, the messages section) and what is its exit status for a clean vs. a conflicted merge? Try `--name-only` and `--no-messages`. Then do the same for a pair of branches that merge cleanly and use the printed tree with `git commit-tree <tree> -p A -p B -m msg` to create a merge commit WITHOUT checking anything out. Why is this useful on servers / bare repos (no working tree)?
2. Now really merge (`git switch left && git merge right`) three times, aborting in between (`git merge --abort`), with `merge.conflictStyle` set to `merge`, `diff3` and `zdiff3` (`git -c merge.conflictStyle=... merge right`). Paste the conflict hunk each time and explain what the extra `|||||||` section is, and what `zdiff3` trims compared to `diff3`. While in the conflicted state, run `git checkout --conflict=diff3 config.txt` -- what does it do, and how is it different from `git checkout --ours` / `--theirs` and from `git restore --merge`?
3. During that conflict, inspect the three index stages: `git ls-files -u`, `git show :1:config.txt`, `:2:`, `:3:`. Which stage is base / ours / theirs? Resolve with `git merge-file -p` on the three versions (extract them to temp files first) and compare with your manual resolution.
4. Run `git merge --no-commit --no-ff right` on a CLEAN pair: what state are you in afterwards (`git status`, `.git/MERGE_HEAD`)? Finish it with `git commit`. Then compare `git log --oneline main..left`, `git log --oneline --ancestry-path <base>..left`, and (git >= 2.38) `git log --ancestry-path=<commit> --oneline --all`: what does `--ancestry-path` filter out, and when is that useful for "which commits are between this fix and that release"?

## WHAT I RAN

```bash
# TODO: build the lab history (base commit, left/right with one conflicting line)


# Q1: merge-tree --write-tree (+ commit-tree for a clean pair)


# Q2: three conflict styles, checkout --conflict


# Q3: index stages and merge-file


# Q4: merge --no-commit, --ancestry-path
```

## ANSWERS

1. **`merge-tree --write-tree` output, exit codes, and `commit-tree`:**
   TODO

2. **Conflict styles (paste each hunk) and `checkout --conflict`:**
   ```
   TODO: paste the merge / diff3 / zdiff3 hunks
   ```
   TODO: explain the base section, what zdiff3 trims, and --conflict vs --ours/--theirs/restore --merge

3. **Index stages 1 / 2 / 3 and `git merge-file`:**
   TODO

4. **`merge --no-commit` state and `--ancestry-path`:**
   TODO

## ONE-LINE TAKEAWAY

TODO
