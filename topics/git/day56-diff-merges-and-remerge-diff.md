# Day 56, Task 8 -- Git: inspecting merge commits (`--diff-merges`, `-m`, `--cc`, `--remerge-diff`)

## THE TASK

In a SCRATCH repo (`/tmp/day56-lab`, `git init`) build a small history with two merges: one CLEAN merge (branches touched different files) and one merge where you RESOLVED a conflict by hand -- and in that resolution also sneak in an extra change that neither parent had (an "evil merge"). Then answer the questions by actually running the commands -- never in a real project's history.

1. Run plain `git log -p` and `git show <merge>` on both merges. Why does `git log -p` show NO diff for merge commits by default, while `git show` on the conflicted merge shows a strange two-column diff? What is that format (`--cc`, "dense combined"), what do the two `+`/`-` columns mean, and why does it show nothing at all for the clean merge?
2. Compare `git log -p --diff-merges=first-parent` (same as `--first-parent -p` for merges), `--diff-merges=separate` (same as `-m`), and `--diff-merges=combined` (`-c`) on the conflicted merge. For each, say in one sentence what the diff is relative to. Which one would you use to answer "what did this merge bring into main?"
3. Run `git show --remerge-diff <conflicted-merge>` (Git >= 2.36). What does it compare against -- what does Git re-create in memory first? Show how it reveals your hand-written resolution AND the evil extra change, while the clean merge shows an empty remerge-diff.
4. Find every merge in the lab repo that contains changes not explained by its parents: combine `git log --merges --format=%h` with `--remerge-diff` (or `git diff <merge>^1 <merge>` vs. a fresh `git merge-tree --write-tree <merge>^1 <merge>^2`). Write the one-liner / tiny script you used and paste its output.

## WHAT I RAN

```bash
# Lab setup (scratch repo only)
mkdir /tmp/day56-lab && cd /tmp/day56-lab && git init -b main
printf 'a\n' > a.txt; printf 'line1\nline2\nline3\n' > shared.txt
git add . && git commit -m base

# Clean merge: the two sides touch different files
git switch -c feat-b; printf 'b\n' > b.txt; git add b.txt; git commit -m "add b"
git switch main;     printf 'a2\n' >> a.txt; git commit -am "edit a"
git merge --no-edit feat-b                      # -> 13e6370 Merge branch 'feat-b'

# Conflicted merge + evil change
git switch -c feat-c; sed -i 's/line2/line2-from-feature/' shared.txt; git commit -am "feature edits line2"
git switch main;      sed -i 's/line2/line2-from-main/'    shared.txt; git commit -am "main edits line2"
git merge feat-c                                # CONFLICT in shared.txt
printf 'line1\nline2-resolved-by-hand\nline3\n' > shared.txt   # hand resolution
printf 'EVIL\n' >> a.txt                         # evil: neither parent has this
git add . && git commit -m "Merge feat-c (conflict resolved)"  # -> 481761b

# Inspection
git log -p --merges                  # no diffs shown for either merge
git show 13e6370                     # clean merge: header only, no diff
git show 481761b                     # "diff --cc" two-column output
git log -1 -p --diff-merges=first-parent 481761b
git log -1 -p --diff-merges=separate     481761b   # == -m
git log -1 -p --diff-merges=combined     481761b   # == -c
git show --remerge-diff 481761b
git show --remerge-diff 13e6370

# Evil-merge finder (two variants)
for m in $(git log --merges --format=%h); do
  n=$(git show --remerge-diff --format= "$m" | wc -l)
  echo "$m $n $(git log -1 --format=%s "$m")"
done
for m in $(git log --merges --format=%h); do
  t=$(git merge-tree --write-tree "$m^1" "$m^2" | head -1)
  [ "$t" = "$(git rev-parse "$m^{tree}")" ] && echo "$m clean-reproducible" \
    || { echo "$m differs from automatic merge"; git diff --stat "$t" "$m"; }
done
```

Note: `--remerge-diff` needs Git >= 2.36 and `merge-tree --write-tree` needs >= 2.38. The
Git in my local Linux VM is 2.34, so these were run with Git 2.43.

Key output, `git show 481761b` (dense combined):

```
diff --cc shared.txt
index dad2b77,014a5a3..9b5dcce
@@@ -1,3 -1,3 +1,3 @@@
  line1
- line2-from-main
 -line2-from-feature
++line2-resolved-by-hand
  line3
diff --cc a.txt
@@@ -1,2 -1,2 +1,3 @@@
  a
  a2
++EVIL
```

`git show --remerge-diff 481761b`:

```
diff --git a/a.txt b/a.txt
@@ -1,2 +1,3 @@
 a
 a2
+EVIL
diff --git a/shared.txt b/shared.txt
remerge CONFLICT (content): Merge conflict in shared.txt
@@ -1,7 +1,3 @@
 line1
-<<<<<<< 354124d (main edits line2)
-line2-from-main
-=======
-line2-from-feature
->>>>>>> 5c8d9ac (feature edits line2)
+line2-resolved-by-hand
 line3
```

Finder output:

```
481761b 22 Merge feat-c (conflict resolved)
13e6370 0 Merge branch 'feat-b'

481761b differs from automatic merge
 a.txt      | 1 +
 shared.txt | 6 +-----
13e6370 clean-reproducible
```

## MY ANSWERS

1. A merge has two parents, so "the diff of this commit" is ambiguous, and `git log -p` simply skips merges unless you pick a `--diff-merges` mode. `git show` defaults to `--cc` ("dense combined"): it diffs the result against *both* parents at once. There is one prefix column per parent -- column 1 is parent 1 (main), column 2 is parent 2 (feat-c). `- ` means "this line was in parent 1 but not the result", ` -` "was in parent 2 but not the result", and `++` means "this line is in the result but in NEITHER parent". "Dense" means hunks where the result simply equals one of the parents are dropped as uninteresting. In a clean merge every file in the result is identical to one parent or the other, so everything is dropped and `git show 13e6370` prints only the header. The `++EVIL` line in `a.txt` is already a hint: a file the merge had no reason to touch still shows a line no parent had.
2. `--diff-merges=first-parent` diffs the merge against its first parent only, i.e. "what changed on main by merging" (here: the resolved line2 plus EVIL). `--diff-merges=separate` (`-m`) prints two full diffs, one against each parent in turn. `--diff-merges=combined` (`-c`) is the combined format against all parents at once, like `--cc` but without dropping the uninteresting hunks. To answer "what did this merge bring into main?" I would use first-parent (often together with `--first-parent` on the log), because that is exactly the change main experienced.
3. `--remerge-diff` re-does the merge of the two parents in memory with the current merge machinery, conflict markers included, and diffs that automatic result against the commit that was actually recorded. So what it shows is only what a human changed on top of the mechanical merge. For `shared.txt` it shows the conflict-marker block being replaced by `line2-resolved-by-hand` (that is my resolution), and for `a.txt`, which merged with no conflict, it shows `+EVIL`, the change neither parent explains. On the clean merge `13e6370` the re-created merge is identical to the recorded one, so the remerge-diff is empty (0 lines).
4. See the two loops under "WHAT I RAN". The first counts the remerge-diff lines per merge: anything non-zero has human edits on top of the automatic merge (`481761b` has 22, `13e6370` has 0). The second rebuilds the automatic merge tree with `git merge-tree --write-tree` and compares it with the merge commit's tree, then prints a `--stat` for the ones that differ. One caveat: a merge that had a *conflict* will always show up, because its resolution is by definition not automatic. To isolate an evil change from a legitimate resolution I read the remerge-diff itself: hunks that only replace conflict markers are the resolution, while hunks in files/regions without a `remerge CONFLICT` (like `+EVIL` in `a.txt`) are the evil part.
