# Day 56, Task 8 -- Git: inspecting merge commits (`--diff-merges`, `-m`, `--cc`, `--remerge-diff`)

## THE TASK

In a SCRATCH repo (`/tmp/day56-lab`, `git init`) build a small history with two merges: one CLEAN merge (branches touched different files) and one merge where you RESOLVED a conflict by hand -- and in that resolution also sneak in an extra change that neither parent had (an "evil merge"). Then answer the questions by actually running the commands -- never in a real project's history.

1. Run plain `git log -p` and `git show <merge>` on both merges. Why does `git log -p` show NO diff for merge commits by default, while `git show` on the conflicted merge shows a strange two-column diff? What is that format (`--cc`, "dense combined"), what do the two `+`/`-` columns mean, and why does it show nothing at all for the clean merge?
2. Compare `git log -p --diff-merges=first-parent` (same as `--first-parent -p` for merges), `--diff-merges=separate` (same as `-m`), and `--diff-merges=combined` (`-c`) on the conflicted merge. For each, say in one sentence what the diff is relative to. Which one would you use to answer "what did this merge bring into main?"
3. Run `git show --remerge-diff <conflicted-merge>` (Git >= 2.36). What does it compare against -- what does Git re-create in memory first? Show how it reveals your hand-written resolution AND the evil extra change, while the clean merge shows an empty remerge-diff.
4. Find every merge in the lab repo that contains changes not explained by its parents: combine `git log --merges --format=%h` with `--remerge-diff` (or `git diff <merge>^1 <merge>` vs. a fresh `git merge-tree --write-tree <merge>^1 <merge>^2`). Write the one-liner / tiny script you used and paste its output.

## WHAT I RAN

```bash
# TODO: fill in the exact commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
