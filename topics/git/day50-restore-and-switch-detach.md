# Day 50, Task 8 -- Git: detached HEAD, `git switch --detach`, and recovering work

## THE TASK

In a SCRATCH area (`/tmp/day50-lab`) create a repo with 3 commits and work through the questions by actually running things.

1. Run `git switch --detach HEAD~1`. What does `git status` say, and what exactly is "detached HEAD"?
2. Make a new commit while detached, then `git switch main`. What warning do you get, and how is the commit still reachable (hint: `git reflog`)?
3. Show two ways to keep that commit: `git switch -c <name> <sha>` and `git branch <name> <sha>`. When would you prefer `git tag` instead?
4. What is the difference between `git switch -c`, `git switch -C` and `git switch --detach`? What does `git switch -` do?

## WHAT I RAN

```bash
mkdir /tmp/day50-lab && cd /tmp/day50-lab && git init -b main
for i in 1 2 3; do echo $i > f; git add f; git commit -m c$i; done
git switch --detach HEAD~1          # HEAD is now at <sha> c2
git status                          # HEAD detached at <sha>
echo x > g; git add g; git commit -m detached
SHA=$(git rev-parse --short HEAD)
git switch main                     # warning: you are leaving 1 commit behind
git reflog                          # shows the "detached" commit as HEAD@{1}
git switch -c keep $SHA             # or: git branch keep $SHA
git switch -                        # jump back to the previously checked-out branch
```

## MY ANSWERS

1. `git status` prints `HEAD detached at <sha>`. Normally HEAD is a symbolic ref pointing at a branch (`ref: refs/heads/main`), and a new commit moves that branch. Detached HEAD means HEAD holds a raw commit id instead of a branch name, so no branch advances when you commit. It is fine for inspecting history or trying things out.
2. Git warns "you are leaving 1 commit behind, not connected to any of your branches" and prints the sha plus the `git branch <new-branch-name> <sha>` hint. The commit is not deleted: no branch points at it, but the reflog records every move of HEAD, so `git reflog` still lists it (e.g. `HEAD@{1}: commit: detached`). It stays recoverable until reflog expiry (about 30 days for unreachable entries by default) and a later `git gc` prunes it.
3. `git switch -c keep <sha>` creates the branch at that sha and switches to it; `git branch keep <sha>` creates it without switching. Prefer `git tag <name> <sha>` when you only want a fixed, permanent label (a release or a "known good" point) that should never move when new commits are made, whereas a branch advances with each commit.
4. `-c` (`--create`) creates a new branch and fails if the name already exists. `-C` (`--force-create`) creates it or resets an existing branch to the given start point (overwriting where it pointed). `--detach` checks out a commit with no branch at all. `git switch -` switches back to the previous branch (like `cd -`), which is handy for toggling between two branches.
