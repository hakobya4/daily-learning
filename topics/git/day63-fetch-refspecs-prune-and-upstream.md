# Day 63, Task 8 -- Git: fetch refspecs, remote-tracking branches, `--prune`, and `@{upstream}` / `@{push}`

## THE TASK

Day 53 covered the PUSH side of refspecs. Today, do the FETCH side. Work only in SCRATCH repos: create a bare "server" repo (`git init --bare -b main /tmp/day63/server.git`), one clone that plays "a teammate" (`/tmp/day63/alice`) and one clone that is "you" (`/tmp/day63/me`). Keep all config repo-local (no `--global`). Answer the questions by actually running the commands.

1. In `me`, run `git config --get-all remote.origin.fetch` and explain every part of the default refspec `+refs/heads/*:refs/remotes/origin/*` (the `+`, the source side, the destination side, the `*`). Then, from `alice`, push two new branches (`feature/a`, `feature/b`) and a tag `v1`. In `me`, run plain `git fetch` and list what appeared with `git for-each-ref --format='%(refname)' refs/remotes refs/tags`. Did the tag come along, and why (look up "tag auto-following" and `--tags` / `--no-tags`)? What does `.git/FETCH_HEAD` contain afterwards, and what does `git log FETCH_HEAD` show?
2. From `alice`, delete `feature/a` on the server (`git push origin --delete feature/a`) and force-push a rewritten `feature/b` (amend its commit, `git push --force-with-lease`). In `me`, run `git fetch` again: is `origin/feature/a` still there? What does the fetch output line for `feature/b` look like (the `+ abc...def (forced update)` form) and what would have happened WITHOUT the `+` in the refspec (try a one-off `git fetch origin 'refs/heads/feature/b:refs/remotes/origin/feature/b'`)? Then use `git fetch --prune` (and `--dry-run` first) and explain `fetch.prune` / `remote.origin.prune` and the difference with `--prune-tags`.
3. Add a SECOND fetch refspec so that `me` also mirrors only alice's review branches into a separate namespace: e.g. `git config --add remote.origin.fetch '+refs/heads/review/*:refs/remotes/origin-review/*'`. Push `review/x` from alice and fetch. Where did it land (it may land in TWO places -- why)? Then add a NEGATIVE refspec (`^refs/heads/review/*`) to keep it out of `refs/remotes/origin/`. Also try a one-shot fetch straight into a LOCAL branch: `git fetch origin feature/b:tmp-b`. When does that refuse ("non-fast-forward", or "refusing to fetch into branch ... checked out")?
4. Upstream vs. push destination: create a local `work` branch that TRACKS `origin/main` (`git switch -c work --track origin/main`) but should be PUSHED to `origin/work`. Show `git rev-parse --abbrev-ref work@{upstream}` and `work@{push}` under `push.default=simple` vs. `push.default=current` (and with `remote.pushDefault`). What do `git branch -vv`, `git status -sb` and `git rev-list --left-right --count work@{u}...work` report after one local commit and one new commit on the server's `main`? Finally: what do `branch.work.remote` and `branch.work.merge` in `.git/config` look like, and what does `git branch --unset-upstream` change?

## WHAT I RAN

```bash
# TODO: paste the commands you actually ran, grouped by question
```

## WHAT I OBSERVED

1. **Default refspec, tag auto-following, `FETCH_HEAD`:** TODO
2. **Deleted and force-pushed branches, the `+`, `--prune` vs. `--prune-tags`:** TODO
3. **Extra and negative refspecs, fetching into a local branch:** TODO
4. **`@{upstream}` vs. `@{push}`, `push.default`, ahead/behind counts:** TODO

## WHAT SURPRISED ME

- TODO

## ONE-LINE TAKEAWAY

TODO
