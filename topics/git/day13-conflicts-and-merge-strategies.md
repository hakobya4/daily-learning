# Day 13, Task 6 -- Git: merge conflicts, --ours/--theirs, and merge vs. rebase

## THE TASK

In a SCRATCH repo (`/tmp/merge-lab`, `git init -b main`):

1. Commit `app.txt` with three lines (`alpha`, `beta`, `gamma`) on main.
2. Branch `feature`; change line 2 to `beta-feature` and commit. Back on
   main change line 2 to `beta-main` and commit.
3. Merge `feature` into main. What does the conflict marker block look
   like? Resolve it by hand, then `git add` and `git commit`.
4. Abort/redo the merge (`git merge --abort`, `git reset --hard
   HEAD~1` as needed) and try `git merge -X theirs feature`. How does
   `-X theirs` differ from `git merge -s ours feature`?
5. Redo the scenario but integrate with `git rebase main` from
   `feature`. In a rebase, which side is "ours" and which is "theirs"?
   Why does it feel reversed?
6. Enable `git config rerere.enabled true` in the scratch repo and
   explain what it remembers.

## WHAT I RAN

```
mkdir /tmp/merge-lab && cd /tmp/merge-lab && git init -b main
printf 'alpha\nbeta\ngamma\n' > app.txt && git add app.txt && git commit -m base
git switch -c feature
sed -i 's/^beta$/beta-feature/' app.txt && git commit -am "feature edit"
git switch main
sed -i 's/^beta$/beta-main/' app.txt && git commit -am "main edit"
git merge feature            # CONFLICT (content) in app.txt
# edit app.txt by hand, then:
git add app.txt && git commit
git reset --hard HEAD~1      # undo the merge commit
git merge -X theirs feature  # auto-resolves, feature wins on conflicts
git reset --hard HEAD~1
git merge -s ours feature    # merge commit, content untouched
git reset --hard HEAD~1
git switch feature && git rebase main   # conflict again, resolve, git rebase --continue
git config rerere.enabled true
```

## WHAT EACH COMMAND SHOWED (write AFTER)

The plain merge stops with a conflict block in `app.txt`:

```
alpha
<<<<<<< HEAD
beta-main
=======
beta-feature
>>>>>>> feature
gamma
```

Above `=======` is my current branch (main), below it is the branch being
merged. I edit the block to the final text, remove the three marker lines,
`git add`, and `git commit` creates the merge commit.

`git merge -X theirs feature` is a strategy OPTION: git still does a
normal three-way merge and only on conflicting hunks picks the feature
side; non-conflicting changes from both sides are kept. `git merge -s ours
feature` is a strategy: it records a merge commit with feature as a
parent but takes NONE of feature's changes, the tree stays exactly as
main. So `-X theirs` merges content favouring them; `-s ours` merges
history only.

In a rebase, "ours" is the branch being rebased ONTO (main, the upstream
that is being replayed on) and "theirs" is my own feature commit that is
currently being re-applied. It feels reversed because rebase checks out
main and cherry-picks my commits one by one on top, so my own work is the
"incoming" side.

rerere (reuse recorded resolution) stores the conflict's pre-image and the
resolution I made in `.git/rr-cache`. If the same conflict appears again
(a repeated rebase or re-doing a merge), git applies my earlier resolution
automatically.

## WHEN I WOULD USE EACH (write in your own words)

Merge commit: shared or long-lived branches, when history of the
integration should be preserved and nobody should have their commits
rewritten. Rebase: my own unpublished feature branch, to get a linear
history before opening a PR; never on commits others already pulled.
`-X theirs`/`-X ours`: only when I know one side is right for all
conflicts and still want the other side's non-conflicting changes.
`-s ours`: to mark a branch as merged without taking its content, for
example retiring an obsolete branch. rerere: whenever I rebase a long
branch repeatedly or keep a long-running integration branch.
