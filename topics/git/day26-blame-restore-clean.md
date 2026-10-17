# Day 26, Task 7 -- Git: `git blame -L`, `git restore --source`, `git clean -n`, `git log --diff-filter`, `git range-diff`

## THE TASK

In a SCRATCH repo (`/tmp/blame-lab`, `git init -b main`, a few commits):

1. How do you see who last changed lines 2-4 of a file (`git blame -L`), and how do you ignore whitespace-only changes (`-w`)?
2. How do you restore ONE file to how it looked two commits ago without moving HEAD (`git restore --source`)? How is that different from `git checkout <commit>`?
3. How do you preview which untracked files and directories `git clean` would delete, before really deleting them?
4. How do you list only the commits that DELETED a file (`git log --diff-filter=D`)?
5. What does `git range-diff` compare, and when would you use it (e.g. after a rebase)?

## WHAT I RAN

```bash
mkdir /tmp/blame-lab && cd /tmp/blame-lab && git init -b main
printf 'one\ntwo\nthree\nfour\n' > a.txt && git add a.txt && git commit -m "add a"
printf 'one\nTWO\nthree\nfour\n' > a.txt && git commit -am "change line 2"
printf 'one\nTWO\n  three\nfour\n' > a.txt && git commit -am "indent line 3"
git blame -L 2,4 a.txt          # who last touched lines 2-4
git blame -w -L 2,4 a.txt       # ignore whitespace-only changes
git restore --source=HEAD~2 a.txt   # file as of two commits ago, HEAD unchanged
git restore --source=HEAD~2 --staged --worktree a.txt   # also update the index
mkdir junk && touch junk/x.tmp new.txt
git clean -n        # dry run: untracked files only
git clean -nd       # dry run: untracked files and directories
git clean -fd       # really delete them
git rm a.txt && git commit -m "remove a"
git log --diff-filter=D --oneline -- a.txt   # commits that deleted a.txt
git log --diff-filter=D --name-only --oneline
git range-diff main~3..main@{1} main~3..main   # compare old vs rewritten series
```

## MY ANSWERS

1. `git blame -L 2,4 a.txt` annotates only lines 2 to 4 with the commit, author and date that last changed each line (`-L 2,+3` and `-L /regex/,+5` also work). Adding `-w` ignores whitespace-only changes, so a line that was merely re-indented is still blamed on the commit that changed its real content. `-M` / `-C` additionally follow lines moved or copied within or across files.
2. `git restore --source=HEAD~2 a.txt` writes that file as it was two commits ago into the working tree only (add `--staged` to also update the index). HEAD and the branch do not move and no other file is touched. `git checkout <commit>` instead moves HEAD to that commit (detached HEAD) and changes the whole tree, unless you use `git checkout <commit> -- file`, which is the older equivalent of restore.
3. `git clean -n` (or `--dry-run`) lists the untracked files that would be removed without deleting anything. Add `-d` to include untracked directories, `-x` to include ignored files. Only once the preview looks right run `git clean -fd`; `-f` is required by default because the deletion is permanent and not recoverable via git.
4. `git log --diff-filter=D --oneline -- path` shows only commits in which that path was Deleted (filters are A added, M modified, R renamed, D deleted, ...). Adding `--name-only` or `--name-status` shows which files were deleted; without a path it lists every commit that deleted anything.
5. `git range-diff` compares two ranges of commits (two versions of a patch series) and shows which commits were kept, changed, added, dropped or reordered, plus the diff-of-diffs for the changed ones. It is used after a rebase or `commit --amend` / force-push to review what really changed between the old and new version of a branch, e.g. `git range-diff main old-branch new-branch`, which is typical when reviewing updated pull requests.
