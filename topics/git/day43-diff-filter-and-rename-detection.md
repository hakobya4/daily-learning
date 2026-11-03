# Day 43, Task 7 -- Git: diff-filter, name-status and rename detection

## THE TASK

In a SCRATCH area (`/tmp/day43-lab`) create a repo with: a commit adding `a.txt` (10+ lines of text) and `b.txt`; a commit that renames `a.txt` to `c.txt` with NO content change; a commit that renames `b.txt` to `d.txt` AND edits about 20% of its lines; a commit that deletes `c.txt`.

1. Which command lists only the commits that DELETED a file? (`git log --diff-filter=...`) What are the letters A, D, M, R, C, T?
2. What does `git show --name-status -M HEAD~1` print for the rename-with-edit, and what is the similarity score (`R087`-style)? What does `-M50%` / `-M90%` change?
3. `git log --follow -- d.txt` vs `git log -- d.txt`: what is different and why does `--follow` only work for a single file?
4. What does `-C` (copy detection) do and when does `-C -C` differ from a single `-C`?
5. How do you turn rename detection off for a diff (`--no-renames`) and what does the same rename look like then?

## WHAT I RAN

```bash
# setup: /tmp/day43-lab, a.txt (12 lines) + b.txt (20 lines); rename a->c; rename b->d + edit 4 lines; delete c
$ git log --diff-filter=D --oneline
78141b0 delete c

$ git show --name-status -M --format=%s HEAD~1
rename b to d with edits

R081	b.txt	d.txt

$ git show --name-status -M90% --format=%s HEAD~1
rename b to d with edits

D	b.txt
A	d.txt

$ git log --follow --oneline -- d.txt
5917e8d rename b to d with edits
f91b934 add a b

$ git log --oneline -- d.txt
5917e8d rename b to d with edits

$ git show --name-status --no-renames --format=%s HEAD~1
rename b to d with edits

D	b.txt
A	d.txt
```

## MY ANSWERS

1. `git log --diff-filter=D --oneline` lists only commits that deleted a file (here "delete c"). Letters: A added, D deleted, M modified, R renamed, C copied, T type changed (e.g. file to symlink). Lowercase letters exclude that kind instead (`--diff-filter=d`).
2. `git show --name-status -M HEAD~1` prints `R081	b.txt	d.txt`: R = rename, 081 = 81% similarity (share of content unchanged). The default threshold is 50%. `-M50%` accepts weaker matches as renames; `-M90%` demands 90% similarity, so my 81% rename falls apart into `D b.txt` + `A d.txt`. A pure rename shows `R100`.
3. `git log -- d.txt` stops at the commit that created the name d.txt, because path limiting only matches that literal path. `git log --follow -- d.txt` keeps going through the rename and also shows the history under b.txt. `--follow` works for a single file only because it re-targets one pathspec as it walks history and detects renames heuristically; it cannot track several paths or a directory.
4. `-C` also detects files that were created as a copy of a file modified in the same commit; `-C -C` additionally looks for copy sources among unmodified files in that commit (and in the parent), which is slower. `-C -C -C` (three) searches all commits too. Same idea in `git blame -C`, for code moved between files.
5. `--no-renames` switches detection off: the rename then shows as `D b.txt` and `A d.txt` and the full file content as removed and added in the patch, instead of a small diff on a single renamed file.
