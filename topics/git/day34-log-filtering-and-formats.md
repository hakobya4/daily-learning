# Day 34, Task 7 -- Git: filtering and formatting `git log`

## THE TASK

In a SCRATCH repo (`/tmp/day34-lab`, `git init -b main`) with a handful of commits that add, modify, rename and delete files, by two different authors, on different days:

1. How do you list only commits by one author (`--author`), within a date window (`--since`/`--until`), or whose message matches a pattern (`--grep`)? How do you combine `--grep` with `--invert-grep` or `--all-match`?
2. What do `--name-status` and `--diff-filter=D` show, and how would you find the commit that deleted `a.txt`?
3. How do you print a custom format with `--pretty=format:` (short hash, author, relative date, subject)? What is the difference between `%h`, `%an`, `%ar` and `%s`?
4. What does `git log --oneline main..feature` vs `feature..main` vs `main...feature` show?
5. How do you show only the commits that touched a path (`-- path`) and follow it across renames (`--follow`)?

## WHAT I RAN

```bash
git init -b main /tmp/day34-lab && cd /tmp/day34-lab
git log --author="alice"
git log --since="2 weeks ago" --until="yesterday"
git log --grep="fix"
git log --grep="fix" --invert-grep
git log --grep="fix" --grep="login" --all-match
git log --name-status
git log --diff-filter=D --name-only --pretty=format:"%h %s" -- a.txt
git log --pretty=format:"%h %an %ar %s"
git log --oneline main..feature
git log --oneline feature..main
git log --oneline main...feature
git log --oneline -- path/to/file
git log --follow --oneline -- new-name.txt
```

## MY ANSWERS

1. `--author=<pattern>` matches author name/email; `--since`/`--until` (e.g. `"2 weeks ago"`, `2026-10-01`) bound commit dates; `--grep=<regex>` matches the commit message. `--grep ... --invert-grep` shows commits that do NOT match. With several `--grep` options the default is OR; `--all-match` requires every pattern to match.
2. `--name-status` lists each changed file with a letter: A added, M modified, D deleted, R rename. `--diff-filter=D` keeps only commits that deleted files, so `git log --diff-filter=D -- a.txt` finds the commit that deleted `a.txt`.
3. `git log --pretty=format:"%h %an %ar %s"` prints a custom line: `%h` abbreviated commit hash, `%an` author name, `%ar` author date relative ("3 days ago"), `%s` subject (first line of the message). `format:` puts separators between entries; `tformat:` terminates each.
4. `main..feature` = commits reachable from feature but not from main (what feature adds). `feature..main` = the reverse. `main...feature` (three dots) = the symmetric difference: commits in either branch but not in both (add `--left-right` to see which side).
5. `git log -- path` limits history to commits touching that path. `git log --follow -- path` also follows the file across renames (works for a single file only), so history before the rename shows up too.
