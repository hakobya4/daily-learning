# Day 31, Task 7 -- Git: `check-ignore`, `ls-files -o`, `archive`, `.gitattributes`, `assume-unchanged`

## THE TASK

In a SCRATCH repo (`/tmp/day31-lab`, `git init -b main`) with a `.gitignore` containing `*.log` and `build/`, a `.gitattributes`, and a few tracked + untracked files:

1. How do you find out WHICH rule in WHICH file ignores a path (`git check-ignore -v`)? What does it print for a path that is not ignored?
2. How do you list untracked files while respecting ignore rules (`git ls-files -o --exclude-standard`)? How do you list the ignored ones instead (`-i`)?
3. How do you export a clean snapshot of `HEAD` as a tarball without the `.git` directory (`git archive`)? How does `export-ignore` in `.gitattributes` change it?
4. What does `* text=auto` / `*.sh text eol=lf` in `.gitattributes` do, and why does it matter on a Windows + Linux team?
5. What do `git update-index --assume-unchanged` and `--skip-worktree` do, how do they differ from `.gitignore`, and how do you undo them (`git ls-files -v` shows them)?

## WHAT I RAN

```bash
# TODO: paste the exact commands you ran in the scratch repo
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
