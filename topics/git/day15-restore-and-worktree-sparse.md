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
cd /tmp/restore-lab && git init -b main
for i in 1 2 3 4 5 6; do echo "line $i"; done > notes.txt
git add . && git commit -m init
sed -i 's/line 2/line 2 edited/; s/line 5/line 5 edited/' notes.txt
git add -p notes.txt        # s (split), y for the line-2 hunk, n for line 5
git commit -m "stage line 2 only"
git status --short          # " M notes.txt"
git restore notes.txt       # discard the line-5 change
echo "line 3 changed" >> notes.txt && git add notes.txt
git restore --source=HEAD~1 --staged --worktree notes.txt
git switch -c experiment    # commit something
git switch -                # back to main
echo junk > junk.txt
git clean -n                # "Would remove junk.txt"
git clean -f
```

## WHAT I SAW / ANSWERS

Step 2: after `git add -p` with `s` to split the big hunk and `y`/`n`
answers, only the line-2 change was committed. `git status` showed
` M notes.txt` (modified, NOT staged) for the leftover line-5 change, so
the same file is partly committed and partly still just a working-tree edit.

Step 3: `git restore notes.txt` copies the index version back into the
working tree, throwing away the unstaged line-5 edit (it cannot be undone).
To unstage instead, `git restore --staged notes.txt` moves the file out of
the index but keeps my edits in the working tree.

Step 4: `--source=HEAD~1` says "take the content from the previous commit"
instead of the default (index / HEAD). `--staged` writes that content into
the index; `--worktree` writes it into the working file. With both, the file
and the index both become the HEAD~1 version (line 2 back to the original, my
extra line gone), and HEAD itself doesn't move. Afterwards `git status` shows
`M  notes.txt` (staged), because that version differs from HEAD.

Step 5: `git switch -c experiment` creates and moves to a branch. `-` means
"the previously checked-out branch" (like `cd -`), so it took me back to
main. `git switch` only changes branches, while `git restore` only changes
files; the old `git checkout` did both jobs, which made mistakes easy (e.g.
a typo'd branch name being treated as a file path).

Step 6: `git clean -n` is a dry run that lists what would be deleted
("Would remove junk.txt"). Always dry-run first because `clean -f` deletes
untracked files permanently - they're not in any commit, so there is no
reflog or other way to get them back.

## DONE WHEN

All steps run in a scratch repo and every TODO above is replaced.
