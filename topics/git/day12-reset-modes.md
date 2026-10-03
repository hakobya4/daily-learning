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

rm -rf /tmp/reset-lab && mkdir /tmp/reset-lab && cd /tmp/reset-lab
git init -b main
for i in 1 2 3 4; do echo "line $i" >> notes.txt; git add notes.txt; git commit -m "c$i"; done
git reset --soft HEAD~2
git status --short          # M  notes.txt (staged)
git commit -m "c3+c4 combined"
git reset --mixed HEAD~1    # same as: git reset HEAD~1
git status --short          # " M notes.txt" (unstaged)
git add notes.txt && git commit -m "c3+c4 again"
git reset --hard HEAD~1
git reflog
git reset --hard HEAD@{1}   # get the commit back
git revert HEAD --no-edit
git restore notes.txt
git restore --staged notes.txt

## WHAT EACH COMMAND SHOWED (write AFTER)

- `--soft`: moves only the branch pointer (HEAD). The changes of c3 and c4 stay in the index (staged), and the working tree is untouched, so I can re-commit them as one commit.
- `--mixed`: moves HEAD and resets the index, but keeps the working tree. Nothing is staged any more; the changes are still in the file as unstaged modifications.
- `--hard` and recovery: moves HEAD, resets the index AND overwrites the working tree, so the changes disappear from the file. The commit is not deleted, only unreachable: `git reflog` still lists it and `git reset --hard HEAD@{1}` (or `git branch rescue <sha>`) brings it back. Uncommitted work lost by --hard is NOT recoverable this way.
- `revert` vs `reset` on shared branches: revert adds a NEW commit that undoes an earlier one, so history only moves forward and nobody has to rewrite anything. Reset rewrites history; after pushing, teammates who already have the old commits would need a force-push and would hit diverged branches. So revert is right on pushed/shared branches.
- `restore` vs `reset`: `git restore <file>` discards working-tree changes of that file (back to the index); `git restore --staged <file>` unstages it (index back to HEAD) and keeps the edits. Unlike reset they act on files, not on the branch pointer, so no commits move.

## WHEN I WOULD USE EACH (write in your own words)

- `reset --soft`: I want to redo or squash the last few local commits (fix a message, combine commits) before pushing.
- `reset --mixed`: I want to unstage things / split a commit into smaller ones, keeping my edits.
- `reset --hard`: throw away local commits and changes completely, only when I am sure (reflog is the safety net for commits).
- `revert`: undo a commit that is already pushed or shared.
- `restore`: discard edits in a file or unstage a file without touching history.
