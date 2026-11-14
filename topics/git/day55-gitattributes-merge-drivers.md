# Day 55, Task 8 -- Git: `.gitattributes` merge drivers, `check-attr` and `merge-tree`

## THE TASK

In a SCRATCH repo (`/tmp/day55-lab`, `git init`, a couple of branches that edit the same files) explore how attributes change merge behaviour. Work through the questions by actually running things -- never in a real project's history.

1. Create a `CHANGELOG.md` that two branches both append a line to at the end, and merge them -- you get a conflict. Now add `CHANGELOG.md merge=union` to `.gitattributes`, redo the merge (reset first), and show the result. What does the built-in `union` driver do with the two sides, and why is it dangerous for files where order or uniqueness matters (e.g. a JSON file)?
2. Mark a generated file (e.g. `package-lock.json` or a fake `build/version.txt`) with `merge=ours`. Merge a branch that changed it. Does `merge=ours` do anything on its own? What extra config does it need (`git config merge.ours.driver true`), and how is this different from `git merge -s ours` and from `-X ours`?
3. Write a tiny custom merge driver in the scratch repo's LOCAL config (`merge.<name>.name` / `merge.<name>.driver` using the `%O %A %B %P` placeholders -- e.g. a script that keeps the numerically larger value in `VERSION`). Which file must the driver write its result to, and what must its exit status be to signal a conflict?
4. Use `git check-attr -a <path>` and `git check-attr merge -- <paths>` to show which attributes apply, including one inherited from a pattern in a subdirectory's `.gitattributes`. Then use `git merge-tree --write-tree <branch1> <branch2>` (Git >= 2.38) to compute a merge WITHOUT touching the working tree or index: what does it print on a clean merge vs. a conflicting one, and what is its exit code in each case?

## WHAT I RAN

```bash
# TODO: fill in the exact commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
