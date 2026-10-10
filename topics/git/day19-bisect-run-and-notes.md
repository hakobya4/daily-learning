# Day 19, Task 7 -- Git: `bisect run`, `git notes`, `commit --fixup`, `blame -L`

## THE TASK

In a SCRATCH repo (`/tmp/bisect-lab`, `git init -b main`):

1. Make 8 commits that append a line to `f.txt`; make commit 5 add the line `BUG`. Write a script `check.sh` (outside the repo) that exits 1 if `f.txt` contains `BUG`, else 0.
2. Use `git bisect start`, `git bisect bad HEAD`, `git bisect good <first commit>` and `git bisect run ../check.sh` to find the first bad commit automatically. What does the output look like and how do you end the session?
3. Attach a note to a commit with `git notes add -m "..." <commit>`. How do you show it in `git log`, and why do notes not change the commit hash?
4. Fix a typo in an earlier commit's file using `git commit --fixup <commit>` and then `git rebase -i --autosquash`. What does the fixup commit message look like before the autosquash?
5. What does `git blame -L 3,5 f.txt` show, and how do you ignore a pure-formatting commit with `--ignore-rev`?

## WHAT I RAN

```
git init -b main /tmp/bisect-lab && cd /tmp/bisect-lab
for i in 1 2 3 4 5 6 7 8; do
  if [ $i -eq 5 ]; then echo BUG >> f.txt; else echo "line $i" >> f.txt; fi
  git add f.txt; git commit -m "commit $i"
done
printf '#!/bin/sh\n! grep -q BUG f.txt\n' > /tmp/check.sh && chmod +x /tmp/check.sh
git bisect start
git bisect bad HEAD
git bisect good $(git rev-list --max-parents=0 HEAD)
git bisect run /tmp/check.sh
git bisect reset
git notes add -m "reviewed by me" HEAD~2
git log --notes -3
git commit --fixup HEAD~3          # after fixing a typo and git add
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash --root
git blame -L 3,5 f.txt
git blame --ignore-rev <format-commit-sha> f.txt
```

## MY ANSWERS

1. Done in the scratch repo: 8 commits appending to `f.txt`, commit 5 adds `BUG`, and `check.sh` lives outside the repo (here `/tmp/check.sh`) so checkouts during bisect never touch it.
2. `git bisect start`, `git bisect bad HEAD`, `git bisect good <first commit>`, then `git bisect run /tmp/check.sh`. Git checks out the midpoint, runs the script, treats exit 0 as good and 1-124 (except 125) as bad, and repeats in about log2(n) steps. The output ends with `<sha> is the first bad commit` followed by the commit message of "commit 5" and the changed file. Exit code 125 means "cannot test, skip this commit". End the session with `git bisect reset`, which returns to the branch you started on.
3. `git notes add -m "reviewed by me" <commit>` stores the note as a blob in a separate ref (`refs/notes/commits`), attached to the commit's hash. `git log` shows notes by default (`--notes` makes it explicit). The commit hash does not change because the note is not part of the commit object; it lives in its own ref. The catch: notes are not pushed or fetched by default (push `refs/notes/*` explicitly) and are lost on rebase unless `notes.rewriteRef` is configured.
4. Fix the file, `git add` it, then `git commit --fixup <commit>`. The new commit's message is `fixup! <subject of the target commit>`. Then `git rebase -i --autosquash <base>` (or `--root`) reorders the todo list so each fixup sits right after its target with the `fixup` action, and squashing it in discards its message. (`--squash` is similar but keeps the message for editing; `git config rebase.autoSquash true` makes it the default.)
5. `git blame -L 3,5 f.txt` shows, for lines 3 to 5 only, the commit sha, author, date and line number that last changed each line. To skip a pure-formatting commit, run `git blame --ignore-rev <sha> f.txt`, or list shas in a file (such as `.git-blame-ignore-revs`) and use `--ignore-revs-file` or `git config blame.ignoreRevsFile .git-blame-ignore-revs`. Blame then attributes those lines to the earlier real change.
