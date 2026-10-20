# Day 29, Task 7 -- Git: `log --follow`, `blame -w -C`, `commit --fixup`, `rebase --exec`, `includeIf`

## THE TASK

In a SCRATCH repo (`/tmp/day29-lab`, `git init -b main`, a few commits):

1. A file was renamed (`git mv old.txt new.txt`). How do you see its history ACROSS the rename (`git log --follow`)? Why does plain `git log -- new.txt` stop at the rename?
2. What do `git blame -w` and `git blame -C` ignore/detect, and when is each useful (re-indented code, code moved between files)?
3. How do you create a commit that is meant to be squashed into an earlier commit (`git commit --fixup=<rev>`), and how does `git rebase -i --autosquash` use it?
4. How do you run the test command after EVERY commit of a branch during a rebase (`git rebase --exec`), and what happens when one fails?
5. How can you use a different `user.email` for repos under `~/work/` only (`includeIf "gitdir:..."` in `~/.gitconfig`)? How do you verify which value wins (`git config --show-origin --get user.email`)?

## WHAT I RAN

```bash
git init -b main /tmp/day29-lab && cd /tmp/day29-lab
echo one > old.txt && git add old.txt && git commit -m "add old"
git mv old.txt new.txt && git commit -m "rename to new"
echo two >> new.txt && git commit -am "edit new"
git log --oneline -- new.txt            # stops at the rename
git log --follow --oneline -- new.txt   # continues into old.txt
git blame -w -C new.txt
echo three >> new.txt && git commit -am "bug" && echo four >> new.txt && git commit -am "more"
echo fix >> new.txt && git commit -a --fixup=HEAD~1
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash HEAD~4
git rebase --exec "test -f new.txt" HEAD~3
git config --show-origin --get user.email
```

## MY ANSWERS

1. `git log --follow -- new.txt` detects the rename (by content similarity) and keeps listing commits that touched the file under its old name. Plain `git log -- new.txt` filters by the current path only, so history ends at the commit that created that path (the rename). `--follow` works for a single file only.
2. `blame -w` ignores whitespace changes, so re-indenting or reformatting does not steal the blame from the original author. `blame -C` detects lines moved or copied from other files (repeat -C -C -C for wider search), so blame points at where the code was originally written rather than the commit that moved it. Useful after refactors and file splits.
3. `git commit --fixup=<rev>` makes a commit titled "fixup! <subject of rev>". Running `git rebase -i --autosquash <base>` automatically reorders the todo list so each fixup sits right below its target with the `fixup` action, and squashes it in, discarding its message. (`rebase.autoSquash=true` makes this the default.)
4. `git rebase --exec "<cmd>" <base>` (or `-x`) runs the command after each replayed commit, e.g. `--exec "make test"`. If the command exits non-zero the rebase stops at that commit so you can fix it, amend, and `git rebase --continue`; `--abort` returns to the original state.
5. In `~/.gitconfig`: `[includeIf "gitdir:~/work/"]` with `path = ~/.gitconfig-work`, and in that file `[user] email = me@work.example`. The trailing slash makes the match apply to every repo beneath that directory. `git config --show-origin --get user.email` prints the winning value and the file it came from (later entries override earlier ones, so put includeIf after the default `[user]`).
