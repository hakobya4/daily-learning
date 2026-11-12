# Day 53, Task 8 -- Git: push refspecs, `push.default`, and deleting remote branches

## THE TASK

In a SCRATCH area (`/tmp/day53-lab`) create a bare repo to act as the remote (`git init --bare remote.git`), clone it twice (`alice/` and `bob/`), and make a couple of commits on `main` in `alice`. Work through the questions by actually running things -- never against a real remote.

1. In `alice`, create a local branch `wip-login` and push it so that on the remote it is called `feature/login` (one command, using a `src:dst` refspec). Then push only a specific older commit (by hash) to a new remote branch `snapshot`. What does `git ls-remote origin` show?
2. Compare `push.default` values `simple`, `current`, `upstream` and `matching`: set each in `alice` (local config only, scratch repo) and run a bare `git push` from a branch whose upstream has a DIFFERENT name than the local branch. Which values refuse, and which push where?
3. Delete the remote branch `snapshot` in two different ways (`git push origin --delete ...` and the empty-source refspec `:snapshot`). In `bob`, what does `git branch -r` still show until you run `git fetch --prune`? What does `fetch.prune` do?
4. What does a leading `+` in a refspec mean (e.g. `+wip-login:feature/login`), and how is it different from `--force` and from `--force-with-lease`? Show a case where `+` overwrote a commit `bob` had pushed.

## WHAT I RAN

```bash
# TODO: fill in the exact commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
