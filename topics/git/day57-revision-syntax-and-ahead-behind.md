# Day 57, Task 8 -- Git: revision syntax (`~` vs `^`, `@{u}`, `:/text`, `^{tree}`) and ahead/behind counts

## THE TASK

In a SCRATCH repo (`/tmp/day57-lab`, `git init`) make a history with at least one MERGE commit whose second parent is a side branch of 2-3 commits, and a local branch that tracks a second scratch repo used as its "remote" (`git clone /tmp/day57-lab /tmp/day57-clone`, then commit on both sides so the clone's branch is both ahead of AND behind `origin/main`). Then answer the questions by actually running the commands -- never in a real project's history.

1. On the merge commit `M`: what do `M^`, `M^1`, `M^2`, `M~1`, `M~2`, `M^2~1` and `M^^2` each resolve to? Draw the graph (ASCII is fine) and label every commit you reached. Why is `M^2` != `M~2`? Check each one with `git rev-parse --short`.
2. Use `git rev-parse` to print: the full hash of `HEAD`, the TREE object of `HEAD` (`HEAD^{tree}`), the blob of a file as it was two commits ago (`HEAD~2:path/to/file`), and the most recent commit whose message matches a word (`:/word`). What does `git cat-file -t` say for each? What does `HEAD^{commit}` do on a TAG name (try it on an annotated tag)?
3. In the clone: what do `@`, `@{u}` (`@{upstream}`), `@{push}`, `@{1}` and `main@{yesterday}` (or `@{2.minutes.ago}`) refer to? Which of them come from the REFLOG and are therefore local-only and not shared with anyone?
4. Print how many commits the clone's branch is ahead and behind its upstream with ONE command (`git rev-list --left-right --count @{u}...HEAD`), and explain which number is which and why the THREE-dot range is required here. Then list the actual commits on each side with `git log --oneline --left-right --cherry-mark @{u}...HEAD` and explain the `<`, `>` and `=` markers (make one commit a cherry-pick of the other side's commit so a `=` shows up).

## WHAT I RAN

```bash
# --- the lab repo with a merge -----------------------------------------------
git init -b main /tmp/day57-lab && cd /tmp/day57-lab
echo one > notes.txt && git add . && git commit -m "A: initial notes"
echo two >> notes.txt && git commit -am "B: second line"
git switch -c side
echo s1 > side.txt && git add . && git commit -m "S1: start side work"
echo s2 >> side.txt && git commit -am "S2: more side work"
git switch main
echo three >> notes.txt && git commit -am "C: third line"
git merge --no-ff side -m "M: merge side"
git tag -a v1 -m "release v1"
git log --graph --oneline --all

# Q1: ancestry operators on the merge
for r in 'HEAD^' 'HEAD^1' 'HEAD^2' 'HEAD~1' 'HEAD~2' 'HEAD^2~1' 'HEAD^^2'; do
  printf '%-10s %s\n' "$r" "$(git rev-parse --short "$r")"
done

# Q2: peeling and object lookups
git rev-parse HEAD 'HEAD^{tree}' 'HEAD~2:notes.txt' ':/side' ':/third'
for r in HEAD 'HEAD^{tree}' 'HEAD~2:notes.txt' ':/side' v1 'v1^{commit}'; do
  printf '%-18s %s %s\n' "$r" "$(git rev-parse --short "$r")" "$(git cat-file -t "$r")"
done

# --- the clone, made both ahead of and behind origin/main ---------------------
git clone /tmp/day57-lab /tmp/day57-clone
cd /tmp/day57-lab                                   # "remote" side moves on
echo fix > fix.txt && git add . && git commit -m "U1: add fix file"
echo four >> notes.txt && git commit -am "U2: fourth line"
cd /tmp/day57-clone                                 # local side moves on
echo local > local.txt && git add . && git commit -m "L1: local work"
git fetch
git cherry-pick origin/main~1                       # copy U1 -> a patch-equivalent commit

# Q3: shorthand refs
for r in @ '@{u}' '@{push}' '@{1}' '@{2.minutes.ago}'; do
  printf '%-18s %s\n' "$r" "$(git rev-parse --short "$r")"
done
git reflog -4

# Q4: ahead/behind
git rev-list --left-right --count @{u}...HEAD
git log --oneline --left-right --cherry-mark @{u}...HEAD
git rev-list --left-right --count @{u}..HEAD        # for comparison: two dots
git status -sb | head -1
```

## MY ANSWERS

1. The lab graph (hashes from my run):

   ```
   M   84aa743  M: merge side          (parents: C first, S2 second)
   |\
   | S2 1ab8b6c  S2: more side work
   | S1 f118f45  S1: start side work
   C | face300  C: third line
   |/
   B   4771092  B: second line
   A   75ca811  A: initial notes
   ```

   `M^` = `M^1` = `M~1` = **C** (face300): with no number `^` means `^1`, and `~1` is
   "one step along first parents", so all three are the first parent. `M^2` = **S2**
   (1ab8b6c), the second parent (the tip of the merged side branch). `M~2` = **B**
   (4771092): `~2` means "first parent, twice" (M -> C -> B), i.e. `M^1^1`. `M^2~1` =
   **S1** (f118f45): go to the second parent S2, then one first-parent step back.
   `M^^2` parses as `(M^)^2` = "second parent of C" -- C is an ordinary commit with only
   one parent, so `git rev-parse` fails with `fatal: Needed a single revision`.
   `M^2 != M~2` because `^N` picks *which parent* (a width/sideways move at a merge)
   while `~N` walks *N generations* down first parents (a depth move). They only agree
   for N = 1.

2. `git rev-parse HEAD` printed the full 40-hex id `84aa743ee182a83f5d90314bbd5298ba1681eda3`
   and `git cat-file -t` says `commit`. `HEAD^{tree}` peels the commit to its root tree
   (`a696dc7`, type `tree`). `HEAD~2:notes.txt` looks up the path inside B's tree and
   returns that version of the file (`814f4a4`, type `blob` -- the file had only two
   lines then). `:/side` is the youngest commit reachable from any ref whose message
   matches the regex "side"; it found `M: merge side` (84aa743, `commit`) because the
   merge is newer than S1/S2 -- `:/third` gave C (face300). On the annotated tag, `v1`
   itself resolves to the TAG object (`00c23bf`, type `tag`), while `v1^{commit}` peels
   the tag (recursively, if tags point at tags) until it reaches a commit and returns
   84aa743 (`commit`). That is why scripts write `tag^{commit}` (or `^{}`) when they need
   the commit and not the tag object.

3. In the clone, after the fetch and the cherry-pick:
   * `@` is just `HEAD` (409796f, the cherry-picked U1).
   * `@{u}` / `@{upstream}` is the configured upstream of the current branch,
     `origin/main` (d3b8e51 = U2) -- the remote-tracking ref as of the last fetch.
   * `@{push}` is where `git push` would send this branch; with the default
     `push.default=simple` and no separate push remote it is the same `origin/main`
     (d3b8e51). It differs in triangular workflows (pull from upstream, push to a fork).
   * `@{1}` is "where the current branch was one reflog entry ago" -- eddfdf3 (L1),
     before the cherry-pick moved it.
   * `@{2.minutes.ago}` / `main@{yesterday}` is the branch value at a point in time
     according to the reflog. My reflog was younger than two minutes, so Git warned
     `log for 'main' only goes back to ...` and gave the oldest entry (84aa743, the clone).
   `@{1}` and the `@{<date>}` forms come from the REFLOG: it lives in `.git/logs/`, is
   never pushed or fetched, and expires, so they mean something only in this one clone.
   `@{u}` and `@{push}` come from branch config + remote-tracking refs, not the reflog
   (they are still local in the sense that they reflect your last fetch).

4. `git rev-list --left-right --count @{u}...HEAD` printed `2	2`: the LEFT number counts
   commits reachable from the left side (`@{u}`) but not from HEAD -> I am **behind** by
   2 (U1, U2); the RIGHT number counts commits only reachable from HEAD -> **ahead** by 2
   (L1 and my cherry-pick). `git status -sb` agrees: `[ahead 2, behind 2]`. The
   three-dot range is the *symmetric difference* (everything reachable from exactly one
   side, excluding the merge base 84aa743 and below), which is what lets
   `--left-right` sort commits into two buckets. With two dots, `@{u}..HEAD` means
   "reachable from HEAD but not from @{u}" -- only one side -- so it printed `0	2` and
   the behind count was lost.

   `git log --oneline --left-right --cherry-mark @{u}...HEAD` showed:

   ```
   < d3b8e51 U2: fourth line
   = 409796f U1: add fix file
   = cc088f3 U1: add fix file
   > eddfdf3 L1: local work
   ```

   `<` marks a commit from the left side only (upstream has it, I don't), `>` one from
   the right side only (mine, not pushed). `=` replaces `<`/`>` for commits whose
   *patch-id* matches a commit on the other side: cc088f3 (upstream U1) and 409796f (my
   cherry-pick) are different commits with the same diff. `--cherry-pick` would hide
   them entirely, and `--cherry` (= `--right-only --cherry-mark --no-merges`) is the
   usual "what of mine is not upstream yet" view -- it would show `+ L1` and `= U1`.
