# Day 6, Task 7 -- Git: finding a bug with `git bisect`

## THE TASK

Days 2-5 covered branching/stashing, straight rebase, interactive
rebase/squash, and cherry-pick. This one is about `git bisect`:
binary-searching your OWN commit history to find which commit
introduced a bug, instead of guessing or reading diffs one by one.

1. Create a branch off main: `git checkout -b day6-bisect-practice`.
2. Write a tiny script or function (anywhere in this branch, even a
   throwaway file) that works correctly, and commit it.
3. Make 4-5 more small commits on top that each change the same
   function slightly (refactors, unrelated tweaks) -- but at ONE
   commit in the middle, deliberately introduce a real bug (an off-by-
   one, a flipped comparison, whatever). Keep committing normally
   after that, as if you hadn't noticed.
4. Write a tiny standalone check (a one-line shell command or a script
   with an exit code) that passes when the function is correct and
   fails when the bug is present -- this is what bisect will run
   automatically at each step.
5. Start the bisect: `git bisect start`, then `git bisect bad` (current
   commit has the bug) and `git bisect good <the first commit's hash>`
   (known good).
6. Either answer by hand at each step bisect checks out
   (`git bisect good` / `git bisect bad`), OR automate it entirely with
   `git bisect run <your-check-script>`. Let it narrow down to the
   exact bad commit.
7. Once found, run `git bisect reset` to return to where you started,
   then fix the bug (a new commit, not by rewriting the bad one) and
   push.

## WHAT I RAN

I ran this in a scratch git repo to keep the demo self-contained (not
inside this daily-learning repo's own history). Commands, in order:

```
git init
# calc.sh: sum() { echo $(( $1 + $2 )); }

git add calc.sh && git commit -m "Add calc.sh: sum() adds two integers"   # 4029944, good baseline
# comment wording tweak, unrelated
git commit -am "Tweak comment wording"                                    # 8714057
# THE BUG: flipped + to - inside sum()
git commit -am "Refactor sum() internals"                                 # 8876733 <- bad commit
# formatting tweak, unrelated
git commit -am "Minor formatting tweak"                                   # 494a8c8
# header comment, unrelated
git commit -am "Add file header comment"                                  # 3b64f88 (HEAD)

git log --oneline
# 3b64f88 Add file header comment
# 494a8c8 Minor formatting tweak
# 8876733 Refactor sum() internals
# 8714057 Tweak comment wording
# 4029944 Add calc.sh: sum() adds two integers

# check.sh -- exits 0 if calc.sh's sum() is correct (2+3==5), 1 if buggy:
#   result=$(./calc.sh 2 3)
#   [ "$result" -eq 5 ]

git bisect start
git bisect bad HEAD
git bisect good 4029944
git bisect run ./check.sh

# Bisecting: 1 revision left to test after this (roughly 1 step)
# [8876733...] Refactor sum() internals
# running './check.sh'
# Bisecting: 0 revisions left to test after this (roughly 0 steps)
# [8714057...] Tweak comment wording
# running './check.sh'
# 8876733 is the first bad commit
# commit 8876733
#     Refactor sum() internals
#  calc.sh | 2 +-
#  1 file changed, 1 insertion(+), 1 deletion(-)
# bisect found first bad commit

git bisect reset

# fix as a NEW commit, not by rewriting the bad one:
sed -i 's/\$(( \$1 - \$2 ))/$(( $1 + $2 ))/' calc.sh
git commit -am "Fix sum(): restore + (was flipped to - in 8876733)"       # 51fc35d
./calc.sh 2 3   # -> 5, confirmed fixed
git push
```

`git bisect run` needed only 2 real checkouts (out of 4 candidate
commits between good and bad) to land exactly on 8876733 -- the
commit whose diff shows the `+` silently flipped to a `-`.

## WHAT BISECT IS ACTUALLY FOR (write AFTER doing the steps)

With only 5-6 commits, checking each one by hand really is barely
faster than bisecting -- binary search on n commits takes about
log2(n) checks instead of n, and log2(5) versus 5 isn't a meaningful
time saver when each check is a 5-second manual glance. The payoff
shows up in two situations instead: when the history between "known
good" and "known bad" is large (hundreds of commits -- log2(500) is
about 9 checks instead of 500, which is the entire point), and when
each individual check is itself expensive (a full test suite run, a
slow build, a manual reproduction steps that take minutes), because
then even a modest commit count makes a linear scan too slow to be
practical while log2(n) automated checks stays cheap. `git bisect run`
compounds that further by removing the human from the loop entirely,
so it scales to large histories without someone babysitting every
checkout.

Binary search only works here because of one assumption: the bug was
introduced at some single point and stayed present in every commit
after that (it was never "un-introduced" and then re-introduced
again later). That's what makes "good...bad" a clean boundary you can
narrow in half each time -- if the bug flickered in and out across the
history (present, then accidentally fixed, then reintroduced by an
unrelated change), the good/bad answers wouldn't be monotonic along
the commit line, bisect's halving logic would land on inconsistent
answers, and it could report the wrong commit or fail to converge at
all.
