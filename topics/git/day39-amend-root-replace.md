# Day 39, Task 7 -- Git: amend, rebase --root and replace

## THE TASK

In a SCRATCH area (`/tmp/day39-lab`) create a repo with 3 commits (`A`, `B`, `C`) on `main`, then practice rewriting history.

1. Your latest commit has the wrong author and message. Which single command fixes both the message and resets the author/date to the current config? What changes about the commit (hash? parents? tree?) and why?
2. The mistake is in the very FIRST commit `A` (e.g. a wrong file was committed). Plain `git rebase -i HEAD~N` cannot reach it. Which flag lets you edit the root commit, and what do you mark in the todo list?
3. What does `git commit --amend --no-edit` do versus `git commit --amend -a`? When is `--no-edit` useful?
4. `git replace <old> <new>` lets you swap one commit for another WITHOUT rewriting history. How does it work, how do you see active replacements, and how do you make a replacement permanent (hint: `git replace --graft` / `filter-repo` idea)?
5. After rewriting published history, why must you use `git push --force-with-lease` and not plain `--force`?

## WHAT I RAN

```bash
mkdir /tmp/day39-lab && cd /tmp/day39-lab && git init -b main
echo a > a.txt && git add . && git commit -m "A"
echo b > b.txt && git add . && git commit -m "B"
echo c > c.txt && git add . && git commit -m "C"

git commit --amend --reset-author -m "C: add c.txt"   # new message + author/date from config
git commit --amend --no-edit                          # fold staged changes in, keep message
git rebase -i --root                                  # mark A as "edit", fix it, then:
git commit --amend && git rebase --continue
git replace <old> <new>                               # swap a commit without rewriting
git replace -l                                        # list active replacements
git replace --graft <commit> [<new-parent>...]        # rewrite parents via a replacement
git filter-repo --replace-refs delete-no-add          # (or filter-repo) bake it in for real
git push --force-with-lease origin main
```

## MY ANSWERS

1. `git commit --amend --reset-author -m "new message"` (or without `-m` to open the editor). The commit gets a NEW hash: the hash covers message, author, committer, timestamps, tree and parents, so changing the message/author changes the id. The tree and parent stay the same (unless you also staged changes); the old commit is just orphaned and still reachable via the reflog. It is a rewrite, not an edit.
2. `git rebase -i --root`. Without it the todo list can never include the first commit because it has no parent to rebase onto. In the todo list mark commit A as `edit` (or `reword` if only the message is wrong), fix it, `git commit --amend`, then `git rebase --continue`; the later commits are replayed on top with new hashes.
3. `--amend --no-edit` rewrites the last commit with whatever is currently staged but keeps the existing message, so no editor opens. `--amend -a` first stages all modified tracked files (like `commit -a`) and then amends, and still opens the editor for the message. `--no-edit` is useful for "forgot a file / small fix-up" amends where the message is already right, and in scripts.
4. `git replace <old> <new>` creates a ref under `refs/replace/<old-hash>` pointing to `<new>`. Whenever git reads object `<old>` it transparently uses `<new>` instead, so history looks rewritten locally without changing any existing hashes. `git replace -l` (or `--list`) shows active replacements; `-d` deletes one; `--no-replace-objects` ignores them. Replacement refs are only local unless pushed/fetched explicitly. `git replace --graft <commit> <parents>` makes a replacement commit with different parents. To make it permanent, run `git filter-repo` (older: `git filter-branch`), which rewrites history so the replaced objects are really changed, and then the replace refs are no longer needed.
5. After rewriting published history, the local branch has diverged from the remote, so a normal push is rejected and you need a force. Plain `--force` overwrites the remote branch no matter what is there, so it silently destroys commits a teammate pushed since you last fetched. `--force-with-lease` only overwrites if the remote ref is still where your remote-tracking branch says it is (what you last saw); if someone else pushed in between, it fails and you can fetch and re-check.
