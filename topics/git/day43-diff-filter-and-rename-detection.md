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
# TODO: paste the commands you ran and a short excerpt of the real output
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
