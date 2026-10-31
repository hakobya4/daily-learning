# Day 40, Task 7 -- Git: blame ignore-revs, mailmap and log search

## THE TASK

In a SCRATCH area (`/tmp/day40-lab`) create a repo where one commit is a pure
formatting change (e.g. re-indenting a file) on top of a commit with real logic.

1. `git blame` now blames the formatting commit for every line. Which option and which file (`.git-blame-ignore-revs`) let blame skip it? How do you make git use that file automatically (config key)?
2. The same person committed as `nk@old.com` and `Narek <narek@new.com>`. What is `.mailmap` for, what is one line of it, and which commands honour it (`shortlog`, `log --use-mailmap`, `blame`)?
3. How do you list commits that touched a file's *content* matching a string (`-S`) versus a regex on the diff (`-G`)? When do they give different results?
4. What does `git log --diff-filter=D --name-only` show, and how would you find the commit that deleted `foo.txt`?
5. Difference between `git log A..B` and `git log A...B`.

## WHAT I RAN

```bash
mkdir -p /tmp/day40-lab && cd /tmp/day40-lab && git init -q
printf 'def f(a,b):\n  return a+b\n' > m.py && git add . && git commit -qm "logic"
printf 'def f(a, b):\n    return a + b\n' > m.py && git commit -qam "reformat"
git rev-parse HEAD > .git-blame-ignore-revs
git blame --ignore-revs-file .git-blame-ignore-revs m.py
git config blame.ignoreRevsFile .git-blame-ignore-revs
git log -S"return" --oneline          # commits where the count of "return" changed
git log -G"return\s+a" --oneline      # commits whose diff lines match the regex
git rm -q m.py && git commit -qm "delete m.py"
git log --diff-filter=D --name-only --oneline
git log --diff-filter=D --oneline -- m.py
git log main..feature ; git log main...feature
```

## MY ANSWERS

1. `git blame --ignore-rev <sha>` or `--ignore-revs-file <file>`; the conventional file is `.git-blame-ignore-revs` (one full commit hash per line, `#` comments allowed). To make git use it automatically: `git config blame.ignoreRevsFile .git-blame-ignore-revs` (set per repo, since the file is committed but the config is not). Lines the ignored commit touched are attributed to the previous commit that changed them. GitHub's blame view reads `.git-blame-ignore-revs` by default.
2. `.mailmap` maps alternate names/emails of the same person to one canonical identity, without rewriting history. One line: `Narek <narek@new.com> <nk@old.com>` (canonical name and email first, then the old email to match). `git shortlog` honours it by default; `git log` needs `--use-mailmap` (or `log.mailmap=true`); `git blame` uses it for the displayed author.
3. `-S<string>` (pickaxe) finds commits where the number of occurrences of the string changed (added or removed). `-G<regex>` finds commits whose diff has an added or removed line matching the regex. They differ when a line containing the string moves or is edited without changing the occurrence count: `-S` skips it, `-G` shows it. `-S` with `--pickaxe-regex` treats the argument as a regex, but still counts occurrences.
4. It lists only commits that deleted files (filters `A`dded, `D`eleted, `M`odified, `R`enamed...), and `--name-only` prints the deleted paths. To find who deleted `foo.txt`: `git log --diff-filter=D --oneline -- foo.txt` (the `--` separator is needed because the file no longer exists in the work tree).
5. `A..B` = commits reachable from B but not from A (what B has that A lacks), asymmetric. `A...B` = symmetric difference: commits reachable from either A or B but not from both (add `--left-right` to see which side each came from). For `git diff`, `A...B` instead means diff from the merge base of A and B to B.
