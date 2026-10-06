# Day 15, Task 7 -- Git: restore, switch, and partial staging

## THE TASK

Practice the modern, narrower commands that replaced overloaded
`checkout`, plus hunk-level staging.

In a SCRATCH repo (`/tmp/restore-lab`, `git init -b main`):

1. Commit `notes.txt` with 6 numbered lines ("line 1".."line 6").
2. Edit line 2 AND line 5 (two separate hunks). Use `git add -p` to stage
   ONLY the line-2 hunk (hint: `s` to split, `n`/`y` to answer). Commit it.
   What does `git status` show for the leftover line-5 change?
3. Throw away the line-5 change with `git restore notes.txt`. Which
   command would unstage a staged file instead? (`--staged`)
4. Change a third line, `git add` it, then pull a single file out of an
   OLD commit without moving HEAD: `git restore --source=HEAD~1
   --staged --worktree notes.txt`. Explain what each flag changed.
5. `git switch -c experiment`, commit something, `git switch -` to go
   back. What does `-` mean here? How is `git switch` different from
   `git checkout` for branches vs files?
6. Make a mess with an untracked file, then `git clean -n` (dry run)
   before `git clean -f`. Why always dry-run first?

## WHAT I RAN

```
# TODO: paste the commands you ran
```

## WHAT I SAW / ANSWERS

TODO: answers to the questions in steps 2-6, in your own words.

## DONE WHEN

All steps run in a scratch repo and every TODO above is replaced.
