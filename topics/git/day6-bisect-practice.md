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

TODO: paste the actual commands you ran, in order, including the
`git bisect` output showing it narrowing down commits and the final
"first bad commit" it identified.

## WHAT BISECT IS ACTUALLY FOR (write AFTER doing the steps)

TODO: a few sentences -- with only 5-6 commits, checking each one by
hand isn't much slower than bisecting. At what point (how many commits
back, or how expensive is "checking" a single commit) does
`git bisect run` with an automated check actually start saving real
time over a linear search? Why is a binary search the right strategy
here at all -- what does it assume about the bug (hint: that it was
introduced at some point and never "un-introduced" later)?
