# Day 22, Task 7 -- Git: `revert -m`, `commit --fixup`, `reflog expire`, `git notes`

## THE TASK

In a SCRATCH repo (`/tmp/revert-lab`, `git init -b main`):

1. Create `feature`, add two commits, merge it into `main` with `--no-ff`. How do you undo that merge with a new commit (`git revert -m ?`) and why must you give `-m`? What does `-m 1` mean?
2. After that revert, you merge `feature` again and nothing comes in. Why, and how do you get the changes back (revert the revert, or a different approach)?
3. Make a typo commit on `main`, then more commits after it. How do you create a `fixup!` commit for the typo commit and fold it in with `git rebase -i --autosquash`? What does `git commit --fixup=amend:<sha>` add?
4. Attach a note to a commit with `git notes add`. Do notes travel on a normal `git push`? How do you push/fetch them?
5. After a bad rebase you want to permanently drop old reflog entries: which `git reflog expire` and `git gc` flags do that, and why is it dangerous?

## WHAT I RAN

```
mkdir /tmp/revert-lab && cd /tmp/revert-lab && git init -b main
echo a > f && git add f && git commit -m base
git switch -c feature
echo b >> f && git commit -am "feat 1"
echo c >> f && git commit -am "feat 2"
git switch main && git merge --no-ff feature
git revert -m 1 HEAD                      # undo the merge
git merge feature                         # "Already up to date"
git revert <sha-of-the-revert>            # revert the revert, brings changes back
echo typo > t && git add t && git commit -m "add t (typo)"
git commit --fixup <typo-sha>
git rebase -i --autosquash <typo-sha>~1
git commit --fixup=amend:<sha>            # also lets you reword the message
git notes add -m "reviewed" <sha>
git push origin refs/notes/*
git fetch origin refs/notes/*:refs/notes/*
git reflog expire --expire=now --all && git gc --prune=now
```

## MY ANSWERS

1. A merge commit has two (or more) parents, so `git revert <merge>` cannot know which side of the merge to treat as the "mainline" to return to. `-m 1` says "parent number 1 is the mainline", i.e. the branch you were on when you merged (`main`); the revert then undoes everything the merged-in branch (`feature`) brought in, producing a new commit that reverses it. `-m 2` would instead try to undo the mainline's changes relative to the feature branch, which is almost never what you want.
2. Git records the merge as already done: `feature`'s commits are still ancestors of `main`, and the revert is just another commit that undid their content. So `git merge feature` says "Already up to date" and brings nothing. To get the changes back, revert the revert commit (`git revert <revert-sha>`), which re-applies the changes. Alternatively, rebase or cherry-pick the feature commits into new commits (new hashes) and merge those.
3. `git commit --fixup <sha>` creates a commit titled `fixup! <subject of sha>` containing the staged correction. `git rebase -i --autosquash <sha>~1` then automatically moves it right after the target commit and marks it `fixup`, so it is folded in (add `--autosquash` via `rebase.autoSquash=true` to make it the default). `--fixup=amend:<sha>` creates an `amend!` commit that, when squashed, also replaces the target's commit message (the new message is taken from the amend! commit's body), so you can fix the code and the message together.
4. `git notes add -m "text" <sha>` stores a note in a separate ref (`refs/notes/commits`) without changing the commit hash. Notes do NOT travel on a normal `git push` or `git fetch`, since those only handle branches and tags by default. Push them with `git push origin refs/notes/commits` (or `refs/notes/*`) and fetch with `git fetch origin refs/notes/commits:refs/notes/commits`.
5. `git reflog expire --expire=now --all` removes all reflog entries immediately (use `--expire-unreachable=now` to drop only entries pointing to unreachable commits), and `git gc --prune=now` then deletes the now-unreferenced objects. It is dangerous because the reflog is the safety net for recovering from a bad rebase or reset: once the entries are expired and pruned, the lost commits are gone for good (no `git reset --hard HEAD@{n}`).
