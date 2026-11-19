# Day 59, Task 8 -- Git: dry-run merges with `merge-tree --write-tree`, conflict styles (`merge` / `diff3` / `zdiff3`), and `--ancestry-path`

## THE TASK

In a SCRATCH repo (`/tmp/day59-lab`, `git init -b main`) create a file `config.txt` with ~10 lines and commit it. Branch `left` and `right` off that commit; on each, change the SAME line differently (a real conflict) and on `right` also change a line far away (a clean change). Add one more commit on `main` that touches a different file. Then answer the questions by actually running the commands -- never in a real project's history.

1. Without touching the working tree or index, ask git whether `left` and `right` would merge cleanly: `git merge-tree --write-tree left right`. What does it print on stdout (the first line, the "Conflicted file info" section, the messages section) and what is its exit status for a clean vs. a conflicted merge? Try `--name-only` and `--no-messages`. Then do the same for a pair of branches that merge cleanly and use the printed tree with `git commit-tree <tree> -p A -p B -m msg` to create a merge commit WITHOUT checking anything out. Why is this useful on servers / bare repos (no working tree)?
2. Now really merge (`git switch left && git merge right`) three times, aborting in between (`git merge --abort`), with `merge.conflictStyle` set to `merge`, `diff3` and `zdiff3` (`git -c merge.conflictStyle=... merge right`). Paste the conflict hunk each time and explain what the extra `|||||||` section is, and what `zdiff3` trims compared to `diff3`. While in the conflicted state, run `git checkout --conflict=diff3 config.txt` -- what does it do, and how is it different from `git checkout --ours` / `--theirs` and from `git restore --merge`?
3. During that conflict, inspect the three index stages: `git ls-files -u`, `git show :1:config.txt`, `:2:`, `:3:`. Which stage is base / ours / theirs? Resolve with `git merge-file -p` on the three versions (extract them to temp files first) and compare with your manual resolution.
4. Run `git merge --no-commit --no-ff right` on a CLEAN pair: what state are you in afterwards (`git status`, `.git/MERGE_HEAD`)? Finish it with `git commit`. Then compare `git log --oneline main..left`, `git log --oneline --ancestry-path <base>..left`, and (git >= 2.38) `git log --ancestry-path=<commit> --oneline --all`: what does `--ancestry-path` filter out, and when is that useful for "which commits are between this fix and that release"?

## WHAT I RAN

```bash
# Lab history (scratch repo only; git 2.43 -- merge-tree --write-tree and
# --ancestry-path=<commit> need >= 2.38, zdiff3 needs >= 2.35)
git init -b main /tmp/day59-lab && cd /tmp/day59-lab
printf '%s\n' 'name = demo' 'port = 8080' 'host = localhost' 'debug = false' 'workers = 4' \
  'timeout = 30' 'retries = 3' 'log = info' 'cache = on' 'theme = light' > config.txt
git add config.txt && git commit -m base                       # ef922e2
git switch -c left
sed -i 's/^port = 8080/port = 9090/' config.txt && git commit -am "left: port 9090"
git switch main && git switch -c right
sed -i -e 's/^port = 8080/port = 7070/' -e 's/^theme = light/theme = dark/' config.txt
git commit -am "right: port 7070, dark theme"                  # conflicting + clean change
git switch main && echo readme > README.md && git add README.md && git commit -m "main: readme"
git switch -c clean ef922e2                                     # a branch that merges cleanly with right
sed -i 's/^log = info/log = debug/' config.txt && git commit -am "clean: log debug"
git log --graph --oneline --all

# Q1: merge-tree --write-tree (+ commit-tree for a clean pair)
git merge-tree --write-tree left right; echo "exit=$?"
git merge-tree --write-tree --name-only left right
git merge-tree --write-tree --no-messages left right
git merge-tree --write-tree clean right; echo "exit=$?"
T=$(git merge-tree --write-tree clean right)
M=$(git commit-tree "$T" -p clean -p right -m "merge right into clean (no checkout)")
git log --oneline --graph -3 "$M"; git status --short          # working tree untouched
# (to keep it: git update-ref refs/heads/clean "$M")

# Q2: three conflict styles, checkout --conflict
git switch left
for s in merge diff3 zdiff3; do
  git -c merge.conflictStyle=$s merge right
  sed -n '/^<<<<<<</,/^>>>>>>>/p' config.txt
  git merge --abort
done
# extra pair to see what zdiff3 trims: both sides also make the SAME change to the
# neighbouring "host" line
git switch -c zl ef922e2 && sed -i -e 's/^port = 8080/port = 9090/' -e 's/^host = localhost/host = 0.0.0.0/' -e 's/^workers = 4/workers = 8/' config.txt && git commit -am zl
git switch -c zr ef922e2 && sed -i -e 's/^port = 8080/port = 7070/' -e 's/^host = localhost/host = 0.0.0.0/' -e 's/^workers = 4/workers = 16/' config.txt && git commit -am zr
git switch zl && git -c merge.conflictStyle=diff3  merge zr; git merge --abort
git switch zl && git -c merge.conflictStyle=zdiff3 merge zr; git merge --abort
git switch left && git merge right                              # stay conflicted
git checkout --conflict=diff3 config.txt
git checkout --ours config.txt;  grep -E 'port|theme' config.txt; git status --short
git restore --merge config.txt;  git status --short

# Q3: index stages and merge-file
git ls-files -u
for n in 1 2 3; do git show :$n:config.txt | grep port; done
git show :1:config.txt > /tmp/base.txt
git show :2:config.txt > /tmp/ours.txt
git show :3:config.txt > /tmp/theirs.txt
git merge-file -p /tmp/ours.txt /tmp/base.txt /tmp/theirs.txt; echo "exit=$?"
git merge-file -p --theirs /tmp/ours.txt /tmp/base.txt /tmp/theirs.txt | grep -E 'port|theme'
git merge-file -p --union  /tmp/ours.txt /tmp/base.txt /tmp/theirs.txt | grep -E 'port|theme'
# manual resolution: keep 7070, drop markers
sed -i -e '/^<<<<<<</d' -e '/^=======/d' -e '/^>>>>>>>/d' -e '/^port = 9090/d' config.txt
git add config.txt && git commit -m "Merge right into left (port 7070)"

# Q4: merge --no-commit, --ancestry-path
git switch clean && git merge --no-commit --no-ff right
git status; cat .git/MERGE_HEAD; git log --oneline -1
git commit --no-edit && git log --oneline --graph -4
git switch left
git log --oneline main..left
git log --oneline --ancestry-path ef922e2..left
git log --oneline 00241ad..left
git log --oneline --ancestry-path 00241ad..left
git log --oneline --ancestry-path=ba32a92 --all
```

## ANSWERS

1. **`merge-tree --write-tree` output, exit codes, and `commit-tree`:**
   `git merge-tree --write-tree left right` performs the whole merge (merge-base lookup,
   ort strategy, rename detection) purely in the object database. Stdout for the
   conflicted pair:

   ```
   7aaf3d8ed3c323dc2b9bb472d7e665cffa8bd0fb                       <- tree OID of the result
   100644 a5c6f812... 1	config.txt                                <- "Conflicted file info":
   100644 9b29be1d... 2	config.txt                                   mode, blob, STAGE, path
   100644 4a0c1709... 3	config.txt                                   (like ls-files -u)

   Auto-merging config.txt                                         <- informational messages
   CONFLICT (content): Merge conflict in config.txt
   ```

   The first line is always a tree OID -- even with conflicts it is written, and the
   conflicted files inside it contain the usual `<<<<<<<` markers. Exit status is **0 for a
   clean merge, 1 for conflicts** (and >1 for real errors such as a bad revision), so a
   script can just test `$?`. `--name-only` shrinks the conflicted-file section to bare
   paths (`config.txt`); `--no-messages` drops the blank line and the
   "Auto-merging / CONFLICT" messages, leaving tree + stage lines. For the clean pair
   (`clean` + `right`) stdout is only the tree OID `1bb8bfc...` and exit 0.

   `git commit-tree <tree> -p clean -p right -m msg` then wraps that tree in a commit with
   two parents and prints its OID (`0f7afd2`, graph shows the two parents) -- `HEAD`, the
   index and the working tree are untouched (`git status` still clean, still on `clean`),
   and no branch moves until you `git update-ref refs/heads/<branch> <commit>`. That is
   exactly what a server needs: bare repositories have no working tree, so a forge can
   answer "is this PR mergeable?", compute the conflict list, or create the merge commit
   for a "merge" button without checking anything out, without locking a worktree and
   in parallel for many PRs. It also makes CI pre-merge checks cheap.

2. **Conflict styles (paste each hunk) and `checkout --conflict`:**
   ```
   merge (default)         diff3                    zdiff3 (same here)
   <<<<<<< HEAD            <<<<<<< HEAD             <<<<<<< HEAD
   port = 9090             port = 9090              port = 9090
   =======                 ||||||| ef922e2          ||||||| ef922e2
   port = 7070             port = 8080              port = 8080
   >>>>>>> right           =======                  =======
                           port = 7070              port = 7070
                           >>>>>>> right            >>>>>>> right

   zl/zr pair (both sides ALSO changed host -> 0.0.0.0 identically):
   diff3                    zdiff3
   <<<<<<< HEAD             <<<<<<< HEAD
   port = 9090              port = 9090
   host = 0.0.0.0           ||||||| ef922e2
   ||||||| ef922e2          port = 8080
   port = 8080              host = localhost
   host = localhost         =======
   =======                  port = 7070
   port = 7070              >>>>>>> zr
   host = 0.0.0.0           host = 0.0.0.0      <- moved OUT of the conflict
   >>>>>>> zr
   ```
   The `|||||||` section (labelled with the merge base, here `ef922e2`) shows what the
   lines looked like in the **common ancestor**. With only ours/theirs you see "9090 vs.
   7070" but not who changed what; with the base you can see that BOTH sides changed it
   from 8080, i.e. a real decision is needed (if one side still had 8080 git would have
   auto-merged it). Plain `merge` style can't tell you that.
   `zdiff3` ("zealous diff3") additionally trims lines that are **identical on both sides**
   at the start/end of the conflicting region and moves them outside the markers (the
   `host = 0.0.0.0` line above), so the hunk only contains the lines that really differ.
   The base section stays complete -- it still shows the base's `host = localhost`. When
   there is nothing common to trim (the first pair), `diff3` and `zdiff3` look the same.

   `git checkout --conflict=diff3 config.txt` re-creates the conflicted file from the
   three index stages in the requested style ("Recreated 1 merge conflict"; markers are
   labelled `ours` / `base` / `theirs`). Handy if you started with `merge` style, or
   botched a manual resolution and want to start over. It only works while the stages
   still exist (before `git add`). `--ours` / `--theirs` instead take the WHOLE file from
   stage 2 / 3 -- no markers, and careful: `--ours` gave `port = 9090` **and**
   `theme = light`, i.e. it also threw away right's clean, non-conflicting theme change.
   The file stays unmerged (`UU`) until `git add`. `git restore --merge config.txt` is the
   modern equivalent of `checkout -m`: it re-creates the conflict markers from the stages
   using the configured / default style (here `merge`, without base), or `--conflict=diff3`
   to pick one.

3. **Index stages 1 / 2 / 3 and `git merge-file`:**
   `git ls-files -u` lists one line per stage for every unmerged path (same three lines
   merge-tree printed). **Stage 1 = merge base** (`:1:` has `port = 8080`), **stage 2 =
   ours / HEAD** (`left`, `port = 9090`), **stage 3 = theirs / the branch being merged**
   (`right`, `port = 7070`). Stage 0 is the normal resolved entry; `git add` replaces 1-3
   with a single stage-0 entry (afterwards `ls-files -u` is empty).
   `git merge-file -p ours base theirs` (argument order: current, base, other!) does a
   3-way merge of plain files and prints the result: exactly the same hunk as `git merge`,
   only labelled with the file names (`<<<<<<< /tmp/ours.txt`); exit code = number of
   conflicts (1 here). `--theirs` resolves conflicts to their side but still keeps clean
   changes from both (`port = 7070` + `theme = dark` -- unlike `checkout --theirs`, which
   would also drop ours' clean changes), `--ours` the opposite, and `--union` keeps both
   lines (`port = 9090` and `port = 7070`, which would be wrong for a config file). My
   manual resolution (keep 7070) produced the same file as `merge-file --theirs`, but
   I prefer deciding hunk by hunk.

4. **`merge --no-commit` state and `--ancestry-path`:**
   `git merge --no-commit --no-ff right` on the clean pair prints "Automatic merge went
   well; stopped before committing as requested". The merge result is in the index and
   working tree, but HEAD is still `65c80d5 clean: log debug`. `git status` says "All
   conflicts fixed but you are still merging (use "git commit" to conclude merge)" and
   `.git/MERGE_HEAD` (= `ba32a92`, the other parent) plus `.git/MERGE_MSG` exist. That is
   the moment to inspect or test (or amend the result) before recording it. A plain
   `git commit --no-edit` then creates the two-parent merge commit `7723921`
   (`--no-ff` matters: without it a fast-forward would just move the branch and there
   would be nothing to "stop before").

   `main..left` = commits reachable from left but not from main: the merge, `left: port
   9090` and `right: ...` (the right commit came in through the merge). `--ancestry-path
   ef922e2..left` is identical here because every one of them descends from the base. The
   difference shows with a starting commit on one side: `00241ad..left` lists the merge
   **and** `ba32a92 right`, but `--ancestry-path 00241ad..left` lists **only the merge** --
   it drops commits that are not descendants of `00241ad` (`right` was made in parallel,
   it is not "after" 00241ad). The git >= 2.38 form `--ancestry-path=ba32a92 --all` keeps
   only commits that are ancestors or descendants of `ba32a92`: the two merges that
   contain it (`7723921` into clean, `61c8b12` into left), itself and its ancestor `base`
   -- the unrelated `left`, `clean`, `zl`, `zr`, `main: readme` commits vanish.
   Useful for "a fix landed in commit X -- which merges / releases picked it up?"
   (`git log --ancestry-path=<fix> --merges <fix>..release`) or "what was built on top
   of this commit between it and the release", without the side-branch noise that plain
   `A..B` shows.

## ONE-LINE TAKEAWAY

`git merge-tree --write-tree` + `commit-tree` let you merge without a working tree (exit 1
= conflicts), `diff3`/`zdiff3` show the base so you know who changed what (zdiff3 trims
the identical edges), the index holds base/ours/theirs as stages 1/2/3, and
`--ancestry-path` cuts `A..B` down to commits that really descend from A.
