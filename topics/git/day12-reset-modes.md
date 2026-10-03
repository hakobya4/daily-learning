# Day 12, Task 6 -- Git: reset --soft / --mixed / --hard and undoing safely

## THE TASK

Earlier days covered stash, reflog, bisect and archaeology. This one is
about moving branches and the three modes of `git reset`, versus
`git revert` and `git restore`.

1. In a SCRATCH repo (`/tmp/reset-lab`, `git init -b main`) make 4
   commits on `notes.txt` (c1..c4), each appending one line.
2. Run `git reset --soft HEAD~2`. Where do the changes of c3 and c4
   end up (HEAD / index / working tree)? Re-commit them as one commit.
3. Run `git reset --mixed HEAD~1` (the default mode). What is staged
   now? What is left in the working tree?
4. Stage and commit again, then run `git reset --hard HEAD~1`. What
   happened to the changes? How do you get that commit back? (Hint:
   reflog.)
5. Use `git revert HEAD` instead. How is history different from a
   reset, and why is revert the right choice on a pushed branch?
6. What do `git restore <file>` and `git restore --staged <file>` do
   compared with reset?

## WHAT I RAN

TODO: paste the commands you ran.

## WHAT EACH COMMAND SHOWED (write AFTER)

- `--soft`: TODO
- `--mixed`: TODO
- `--hard` and recovery: TODO
- `revert` vs `reset` on shared branches: TODO
- `restore` vs `reset`: TODO

## WHEN I WOULD USE EACH (write in your own words)

TODO
