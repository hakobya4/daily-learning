# Day 58, Task 8 -- Git: `rebase --rebase-merges` and the todo-list commands (`label`, `reset`, `merge`, `exec`, `break`)

## THE TASK

In a SCRATCH repo (`/tmp/day58-lab`, `git init -b main`) build this history: `main` with 2 commits, then a branch `feature` off `main` that contains its OWN merge -- a sub-branch `feature-ui` (2 commits) merged into `feature` with `--no-ff` -- plus one more commit on `feature` after that merge. Meanwhile add 1-2 new commits on `main`. Then answer the questions by actually running the commands -- never in a real project's history.

1. Rebase `feature` onto the new `main` with a PLAIN `git rebase main`. What happens to the inner merge commit? Draw the graph before and after (`git log --graph --oneline --all`). Undo it with the reflog (`git reset --hard feature@{1}` or `ORIG_HEAD`) and explain which of the two you used and why it is the right one.
2. Now rebase with `git rebase -i --rebase-merges main` (`-r`). Paste the generated todo list and explain every `label`, `reset` and `merge -C <hash>` line. What do `onto` and the auto-generated label names refer to? What does `merge -c` (lower case) do differently from `merge -C`?
3. In the same kind of todo list, insert an `exec make test || false`-style line (use `exec test -f notes.txt` or any command that can fail) after one `pick`, and a `break` after another. What happens when the `exec` command fails and how do you continue? What does `break` do, and how is it different from `edit`?
4. Run `git rebase -r --exec "git log -1 --oneline" main`: where does git insert the `exec` lines in a todo list that contains merges? Then explain `--rebase-merges=rebase-cousins` vs. the default `no-rebase-cousins` (make one commit on `feature-ui` whose parent is NOT a descendant of `feature`'s base to see the difference, or explain from the docs if you cannot reproduce it), and what `git pull --rebase=merges` / `pull.rebase = merges` do.

## WHAT I RAN

```bash
# Lab history (scratch repo only)
git init -b main /tmp/day58-lab && cd /tmp/day58-lab
c(){ echo "$1" > "$1.txt"; git add "$1.txt"; git commit -qm "$1"; }
c m1; c m2
git switch -c feature;    c f1
git switch -c feature-ui; c ui1; c ui2
git switch feature
git merge --no-ff feature-ui -m "Merge branch 'feature-ui' into feature"
c f2
git switch main; c m3; c m4
git switch feature
git log --graph --oneline --all

# Q1: plain rebase, then undo
git rebase main
git log --graph --oneline --all
git reflog -6
git rev-parse --short ORIG_HEAD feature@{1}     # both 732ed2e here
git reset --hard ORIG_HEAD

# Q2: rebase --rebase-merges (todo list printed instead of edited)
GIT_SEQUENCE_EDITOR=cat git rebase -i -r main
git reset --hard ORIG_HEAD

# Q3: exec + break in the todo list (sequence editor = a sed script)
#   sed -i -e '/^pick .* f1$/a exec test -f notes.txt' -e '/^pick .* ui2$/a break' "$1"
GIT_SEQUENCE_EDITOR=./ed.sh git rebase -i -r main   # stops: exec failed
echo notes > notes.txt && git add notes.txt && git commit -m "add notes"
git rebase --continue                               # stops again at the break
git rebase --continue                               # finishes
git reset --hard 732ed2e

# Q4: --exec with -r, then a "cousin" branch forked from m1 and merged into feature
GIT_SEQUENCE_EDITOR=cat git rebase -i -r --exec "git log -1 --oneline" main
git reset --hard 732ed2e
git switch -c cousin ec51f5c && echo c > cousin.txt && git add cousin.txt && git commit -m cousin1
git switch feature && git merge --no-ff cousin -m "Merge branch 'cousin' into feature"
GIT_SEQUENCE_EDITOR=cat git rebase -i -r main                              ; git reset --hard ORIG_HEAD
GIT_SEQUENCE_EDITOR=cat git rebase -i --rebase-merges=rebase-cousins main  ; git reset --hard ORIG_HEAD
```

## ANSWERS

1. **Plain rebase and the inner merge:**
   Before:
   ```
   * 732ed2e f2
   *   eeb7233 Merge branch 'feature-ui' into feature
   |\
   | * 1a49990 ui2
   | * 1dc8e9b ui1
   |/
   * 3455bf0 f1
   | * 5e56b43 m4
   | * d455b76 m3
   |/
   * 91c800d m2
   * ec51f5c m1
   ```
   After `git rebase main`:
   ```
   * 601d6f2 f2
   * 4fe4c01 ui2
   * 4383459 ui1
   * 468bf5b f1
   * 5e56b43 m4
   * d455b76 m3
   | * 1a49990 ui2      <- old commits, now only reachable via feature-ui / reflog
   | * 1dc8e9b ui1
   | * 3455bf0 f1
   |/
   * 91c800d m2
   ```
   A plain rebase **drops merge commits**: it linearises `main..feature` (f1, ui1, ui2, f2)
   and replays every non-merge commit on top of `main`. The merge `eeb7233` simply
   disappears and the history becomes a straight line -- the "this came in as a sub-branch"
   information is lost (if the merge had resolved conflicts, those resolutions would have to
   be redone by hand, commit by commit).

   Undo: the reflog showed `rebase (start)` ... `rebase (finish)`, and both `ORIG_HEAD` and
   `feature@{1}` pointed at `732ed2e`. I used `git reset --hard ORIG_HEAD`, which is right
   *immediately* after the rebase because rebase sets ORIG_HEAD to the tip it started from.
   ORIG_HEAD is fragile though -- the next reset/merge/am overwrites it. `feature@{1}` (the
   *branch* reflog, "where feature was one update ago") is the robust choice: a rebase only
   writes ONE entry into the branch reflog (the finish), so `@{1}` is the pre-rebase tip,
   whereas `HEAD@{1}` would be the last `pick` in the middle of the rebase (here `601d6f2`,
   i.e. the rebased result -- wrong).

2. **The `-r` todo list (`label` / `reset` / `merge -C`):**
   ```
   label onto
   reset onto
   pick 3455bf0 f1
   label branch-point
   pick 1dc8e9b ui1
   pick 1a49990 ui2
   label feature-ui
   reset branch-point # f1
   merge -C eeb7233 feature-ui # Merge branch 'feature-ui' into feature
   pick 732ed2e f2
   ```
   * `label onto` -- names the current HEAD. At the start of a rebase HEAD is the commit we
     rebase *onto* (`main` = m4), so `onto` = the new base. Labels are temporary refs
     (`refs/rewritten/<name>`), deleted when the rebase ends.
   * `reset onto` -- moves HEAD (like `reset --hard`, but refuses to clobber untracked
     files) to the label. Every independent strand of history starts with a `reset`.
   * `pick f1` / `label branch-point` -- replays f1 and remembers the rewritten f1, because
     two strands start there (the mainline of `feature` and the `feature-ui` sub-branch).
     Git auto-names fork points `branch-point` (with `-2`, `-3`... suffixes if needed).
   * `pick ui1`, `pick ui2`, `label feature-ui` -- replays the sub-branch and labels its tip.
     The label name is derived from the merge commit's subject ("Merge branch
     'feature-ui'..."), falling back to names like `onto-2` otherwise -- it is NOT the
     branch ref; the real `feature-ui` branch is left untouched.
   * `reset branch-point # f1` -- jump back to the rewritten f1 (the first parent of the merge).
   * `merge -C eeb7233 feature-ui` -- create a NEW merge commit of HEAD and the
     `feature-ui` label, reusing the message (and authorship) of the original merge
     `eeb7233`. If the original merge had resolved conflicts, git does a real merge again
     (it does not copy the old tree), so the same conflicts may come back -- `rerere` helps.
   * `pick f2` -- the commit after the merge.

   `merge -c <hash>` (lower case) does the same but opens the editor so you can reword the
   reused message; without `-C`/`-c` at all (`merge feature-ui`) git generates a fresh
   "Merge branch ..." message and opens the editor. After the rebase the graph has the same
   shape, just on top of m4 (`2a01cae Merge branch 'feature-ui' into feature`).

3. **`exec` failing and `break` vs `edit`:**
   With `exec test -f notes.txt` after `pick f1` and `break` after `pick ui2`, git stopped with
   `warning: execution failed: test -f notes.txt ... You can fix the problem, and then run
   git rebase --continue`. A failing `exec` (non-zero exit) stops the rebase right AFTER
   that line, with everything before it already applied (here f1 rewritten, HEAD on it).
   You inspect/fix -- I created `notes.txt` and even committed it ("add notes" lands in the
   rewritten history between f1 and the sub-branch) -- then `git rebase --continue`
   proceeds with the next line; the failed exec is NOT re-run. (`git rebase --edit-todo`
   would let you change the remaining lines; `--abort` throws everything away.)
   `break` stops unconditionally at that point ("Stopped at 8214a2b (ui2)"), nothing
   failed and nothing is pending; `git rebase --continue` just resumes. `edit <hash>` is a
   `pick` that then stops so you can `git commit --amend` *that* commit; `break` is a pure
   pause without a commit of its own -- useful e.g. right after a `merge` or `reset`, where
   there is no `pick` to turn into `edit`.

4. **`--exec` placement, `rebase-cousins`, `pull --rebase=merges`:**
   `git rebase -r --exec "git log -1 --oneline" main` put an `exec` line after every
   `pick` AND after the `merge -C` line -- i.e. after each line that creates a commit -- but
   when a strand ends in a `label` (before a `reset`), the `exec` goes before the `label`
   (`pick ui2` / `exec ...` / `label feature-ui`). So the command runs on every rewritten
   commit, including the new merge; it never runs after `label`/`reset` themselves.

   Cousins: I added a branch `cousin` forked from **m1** -- older than the merge base m2,
   so its commit is not a descendant of `feature`'s base -- and merged it into `feature`.
   Default (`--rebase-merges` = `no-rebase-cousins`) generated `reset ec51f5c # m1` /
   `pick cousin1`: the cousin keeps its ORIGINAL fork point m1 (git only rewrites it to the
   extent its parents were rewritten). With `--rebase-merges=rebase-cousins` the line became
   `reset onto` and cousin1 was rebased onto m4 like everything else; in the graph the
   cousin strand then starts from m4 instead of dangling down to m1.

   `git pull --rebase=merges` (or `git config pull.rebase merges`) makes `pull` run
   `git rebase --rebase-merges` instead of a plain rebase, so local merge commits you made
   (e.g. merging a topic branch into your local `feature`) survive the pull instead of being
   flattened. `pull.rebase = true` is the plain, merge-dropping variant.

## ONE-LINE TAKEAWAY

A plain rebase flattens merges away; `git rebase -r` rewrites the whole graph as a little
script of `label` / `reset` / `pick` / `merge -C` commands, and `exec` / `break` let you
test or pause anywhere inside it.
