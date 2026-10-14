# Day 23, Task 7 -- Git: `add -p`, `stash --keep-index`, `git cherry`, `switch --orphan`, `commit --amend --reset-author`

## THE TASK

In a SCRATCH repo (`/tmp/patch-lab`, `git init -b main`):

1. A file has two unrelated edits (a bug fix and a debug print). How do you commit ONLY the bug fix with `git add -p`? What do the answers `y`, `n`, `s`, `e` do?
2. You staged part of your work and want to test just the staged part before committing. How does `git stash push --keep-index` help, and how do you get the rest back?
3. `main` and `feature` both got some of the same changes via cherry-pick. How does `git cherry -v main feature` show which commits of `feature` are not yet applied upstream, and what do `+` and `-` mean?
4. How do you start a brand-new history with no parents inside the same repo (`git switch --orphan`), and when is that useful?
5. You committed with the wrong author. How do you fix the LAST commit with `--amend --reset-author`, and what about the last five?

## WHAT I RAN

```
git init -b main /tmp/patch-lab && cd /tmp/patch-lab
printf 'def f(x):\n    return x + 1\n' > app.py && git add app.py && git commit -m init
# edit app.py: fix the bug AND add a debug print, then:
git add -p app.py            # answer y to the fix hunk, n to the print hunk
git diff --cached            # only the fix is staged
git commit -m "Fix off-by-one"
git add -p app.py && git stash push --keep-index   # stash the unstaged rest, keep index+worktree = staged state
# run tests on the staged-only tree, then:
git stash pop                # bring the unstaged work back
git switch -c feature; git cherry-pick <sha>; git switch main
git cherry -v main feature
git switch --orphan fresh    # new root, empty tree
git commit --amend --reset-author --no-edit
git rebase -r HEAD~5 --exec 'git commit --amend --reset-author --no-edit'
```

## MY ANSWERS

1. `git add -p` walks through each diff hunk and asks what to do. `y` stages this hunk, `n` skips it, `s` splits a hunk into smaller hunks when changes are separated by unchanged lines, and `e` opens the hunk in my editor so I can hand-edit exactly which lines get staged (needed when the fix and the debug print sit on adjacent lines and `s` cannot split them). Also `q` quits and `a`/`d` stage or skip everything left in the file. I stage the bug-fix hunk with `y`, skip the debug print with `n`, check with `git diff --cached`, then commit. The debug print stays in the working tree, unstaged.
2. `git stash push --keep-index` stashes all changes that are not staged (and leaves the index as is), so the working tree matches exactly what I am about to commit. I can run the tests on that clean staged-only state. Afterwards `git stash pop` restores the unstaged changes (`--include-untracked` if I also want new files stashed). It helps catch commits that only work because of unstaged edits lying around.
3. `git cherry -v main feature` compares by patch-id (the diff content), not by commit hash. It lists each commit on `feature` that is not in `main`: a line starting with `+` means no equivalent patch exists upstream yet (not applied), a line starting with `-` means an equivalent patch is already in `main`, for example because it was cherry-picked, even though the hash differs. So the `+` lines are what is still left to cherry-pick or merge.
4. `git switch --orphan <name>` creates a new branch with no parent commit and an empty index and working tree, so the first commit on it starts a completely separate history inside the same repository. It is useful for things like a `gh-pages` branch of generated docs, a clean-slate rewrite, or publishing a snapshot without the old history (for example when the old history contains secrets or huge files).
5. For the last commit: `git commit --amend --reset-author` resets the author to my currently configured `user.name`/`user.email` (and the author date to now; add `--no-edit` to keep the message). For the last five commits amend does not work alone, so I rewrite them with `git rebase -r HEAD~5 --exec 'git commit --amend --reset-author --no-edit'` (or `git rebase -i HEAD~5` and `edit` each). That rewrites history, so those commits get new hashes and need `git push --force-with-lease` if they were already pushed.
