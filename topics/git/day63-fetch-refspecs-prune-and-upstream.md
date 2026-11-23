# Day 63, Task 8 -- Git: fetch refspecs, remote-tracking branches, `--prune`, and `@{upstream}` / `@{push}`

## THE TASK

Day 53 covered the PUSH side of refspecs. Today, do the FETCH side. Work only in SCRATCH repos: create a bare "server" repo (`git init --bare -b main /tmp/day63/server.git`), one clone that plays "a teammate" (`/tmp/day63/alice`) and one clone that is "you" (`/tmp/day63/me`). Keep all config repo-local (no `--global`). Answer the questions by actually running the commands.

1. In `me`, run `git config --get-all remote.origin.fetch` and explain every part of the default refspec `+refs/heads/*:refs/remotes/origin/*` (the `+`, the source side, the destination side, the `*`). Then, from `alice`, push two new branches (`feature/a`, `feature/b`) and a tag `v1`. In `me`, run plain `git fetch` and list what appeared with `git for-each-ref --format='%(refname)' refs/remotes refs/tags`. Did the tag come along, and why (look up "tag auto-following" and `--tags` / `--no-tags`)? What does `.git/FETCH_HEAD` contain afterwards, and what does `git log FETCH_HEAD` show?
2. From `alice`, delete `feature/a` on the server (`git push origin --delete feature/a`) and force-push a rewritten `feature/b` (amend its commit, `git push --force-with-lease`). In `me`, run `git fetch` again: is `origin/feature/a` still there? What does the fetch output line for `feature/b` look like (the `+ abc...def (forced update)` form) and what would have happened WITHOUT the `+` in the refspec (try a one-off `git fetch origin 'refs/heads/feature/b:refs/remotes/origin/feature/b'`)? Then use `git fetch --prune` (and `--dry-run` first) and explain `fetch.prune` / `remote.origin.prune` and the difference with `--prune-tags`.
3. Add a SECOND fetch refspec so that `me` also mirrors only alice's review branches into a separate namespace: e.g. `git config --add remote.origin.fetch '+refs/heads/review/*:refs/remotes/origin-review/*'`. Push `review/x` from alice and fetch. Where did it land (it may land in TWO places -- why)? Then add a NEGATIVE refspec (`^refs/heads/review/*`) to keep it out of `refs/remotes/origin/`. Also try a one-shot fetch straight into a LOCAL branch: `git fetch origin feature/b:tmp-b`. When does that refuse ("non-fast-forward", or "refusing to fetch into branch ... checked out")?
4. Upstream vs. push destination: create a local `work` branch that TRACKS `origin/main` (`git switch -c work --track origin/main`) but should be PUSHED to `origin/work`. Show `git rev-parse --abbrev-ref work@{upstream}` and `work@{push}` under `push.default=simple` vs. `push.default=current` (and with `remote.pushDefault`). What do `git branch -vv`, `git status -sb` and `git rev-list --left-right --count work@{u}...work` report after one local commit and one new commit on the server's `main`? Finally: what do `branch.work.remote` and `branch.work.merge` in `.git/config` look like, and what does `git branch --unset-upstream` change?

## WHAT I RAN

```bash
# setup (git 2.34.1, all config repo-local, scratch dirs under /tmp/day63)
git init --bare -b main /tmp/day63/server.git
git clone /tmp/day63/server.git alice      # empty clone; commit "init" on main, push
git clone /tmp/day63/server.git me

# Q1 -- default refspec, tag auto-following, FETCH_HEAD
git -C me config --get-all remote.origin.fetch
# in alice: commit on feature/a, commit on feature/b, git tag v1 main, push all three
git -C me fetch
git -C me for-each-ref --format='%(refname)' refs/remotes refs/tags
cat me/.git/FETCH_HEAD
git -C me log --oneline FETCH_HEAD
# extra: in alice, tag v2 on a detached commit that no branch contains, push only the tag
git -C me fetch && git -C me tag          # v2 did NOT arrive

# Q2 -- deleted + force-pushed branches, '+', prune
git -C alice push origin --delete feature/a
git -C alice commit --amend -m "fb rewritten" && git -C alice push --force-with-lease origin feature/b
git -C me fetch && git -C me branch -r
git -C me fetch origin 'refs/heads/feature/b:refs/remotes/origin/feature/b'   # no '+'
git -C me fetch                                                              # with '+'
git -C me fetch --prune --dry-run
git -C me fetch --prune
git -C alice push origin --delete v1
git -C me fetch --prune                 # v1 stays
git -C me fetch --prune --prune-tags    # v1 goes

# Q3 -- extra + negative refspecs, fetching into a local branch
git -C me config --add remote.origin.fetch '+refs/heads/review/*:refs/remotes/origin-review/*'
# alice pushes review/x
git -C me fetch
git -C me update-ref -d refs/remotes/origin/review/x
git -C me config --add remote.origin.fetch '^refs/heads/review/*'
# alice pushes a second commit to review/x
git -C me fetch -v
git -C me fetch origin feature/b:tmp-b        # creates local branch
# alice force-pushes feature/b again
git -C me fetch origin feature/b:tmp-b        # rejected, non-fast-forward
git -C me switch tmp-b && git -C me fetch origin +feature/b:tmp-b   # refused: checked out

# Q4 -- @{upstream} vs @{push}
git -C me switch -c work --track origin/main
git -C me rev-parse --abbrev-ref work@{upstream}
git -C me config push.default simple|current|upstream ; git -C me config remote.pushDefault origin
git -C me rev-parse --abbrev-ref work@{push}
# one local commit on work; alice pushes one commit to main; git -C me fetch
git -C me branch -vv
git -C me status -sb
git -C me rev-list --left-right --count work@{u}...work
git -C me config --get-regexp '^branch\.work\.'
git -C me branch --unset-upstream
```

## WHAT I OBSERVED

1. **Default refspec, tag auto-following, `FETCH_HEAD`:** The clone has exactly one
   fetch refspec, `+refs/heads/*:refs/remotes/origin/*`. Left of the colon is the SOURCE
   (refs on the remote: every branch), right is the DESTINATION (where they are stored
   locally: the `origin/` remote-tracking namespace). The `*` is a glob that is
   substituted consistently, so `refs/heads/feature/a` becomes
   `refs/remotes/origin/feature/a` (the `*` matches across `/`). The leading `+` means
   "update the destination even if it is not a fast-forward" -- remote-tracking refs
   should simply mirror the server, even after a force-push.
   Plain `git fetch` printed `* [new branch] feature/a -> origin/feature/a`, the same for
   `feature/b`, and `* [new tag] v1 -> v1`; `for-each-ref` then showed
   `refs/remotes/origin/{HEAD,main,feature/a,feature/b}` and `refs/tags/v1`. The tag came
   along because of **tag auto-following**: by default fetch also downloads any tag that
   points at an object being fetched (or already present locally). `v1` points at
   `main`'s commit, so it followed. A second tag `v2` on a commit no branch contained
   did NOT come -- auto-following only grabs tags whose target is in the fetched
   history. `--tags` fetches all tags (`refs/tags/*:refs/tags/*`) regardless, `--no-tags`
   (or `remote.origin.tagOpt = --no-tags`) disables following.
   `.git/FETCH_HEAD` had one line per fetched ref: `<sha> <TAB> <TAB> branch 'main' of
   /tmp/day63/server` for main (the branch's upstream, i.e. the one `git pull` would
   merge) and `<sha> not-for-merge branch 'feature/a' ...` for everything else, including
   `tag 'v1'`. `git log FETCH_HEAD` resolves to the FIRST line without `not-for-merge`, so
   it showed `init` -- the tip of origin/main.
2. **Deleted and force-pushed branches, the `+`, `--prune` vs. `--prune-tags`:** After
   alice deleted `feature/a` on the server, a normal `git fetch` said nothing about it and
   `origin/feature/a` was STILL listed by `git branch -r` -- fetch never deletes refs
   unless asked. The rewritten `feature/b` showed up as
   ` + b8063ba...ca57936 feature/b  -> origin/feature/b  (forced update)` (three dots and a
   `+` instead of the usual two-dot fast-forward line). The one-off fetch with the same
   refspec minus the `+` was refused: ` ! [rejected] feature/b -> origin/feature/b
   (non-fast-forward)`, exit code 1, and the ref was left untouched.
   `git fetch --prune --dry-run` printed ` - [deleted] (none) -> origin/feature/a` without
   doing it; the real `--prune` removed it. `fetch.prune=true` (all remotes) or
   `remote.origin.prune=true` (one remote) make every fetch behave like `--prune`.
   Prune only deletes refs in DESTINATIONS of the refspecs used, i.e. the remote-tracking
   namespace -- so after alice deleted tag `v1`, `git fetch --prune` kept my local `v1`.
   Only `git fetch --prune --prune-tags` (or `fetch.pruneTags`) deleted it
   (`- [deleted] (none) -> v1`). That is deliberately opt-in because tags live in the
   shared `refs/tags/` namespace and might be your own local tags.
3. **Extra and negative refspecs, fetching into a local branch:** With the second refspec
   `+refs/heads/review/*:refs/remotes/origin-review/*`, pushing `review/x` and fetching
   produced TWO lines: `review/x -> origin/review/x` and `review/x -> origin-review/x`.
   Every refspec is applied independently, and the default `refs/heads/*` also matches
   `refs/heads/review/x`, so it lands in both namespaces.
   I then added the negative refspec `^refs/heads/review/*`. Surprise: it did not just
   keep `review/x` out of `origin/` -- after alice pushed another commit, `git fetch -v`
   didn't mention `review/x` at all and `origin-review/x` stayed on the old commit
   (`cf475a3` vs. the server's `cec9681`). A negative refspec removes matching SOURCE
   refs from the whole fetch, across all refspecs, so it can't be used to route a branch
   into only one of two namespaces. (To get the intended result you'd instead change the
   default refspec, e.g. replace it with explicit patterns that don't cover `review/`.)
   `git fetch origin feature/b:tmp-b` created a local branch: `* [new branch] feature/b ->
   tmp-b`. After another force-push on the server, the same command was rejected
   (`! [rejected] feature/b -> tmp-b (non-fast-forward)`, exit 1) while the default
   refspec still updated `origin/feature/b` with `(forced update)` in the same run. With
   `tmp-b` checked out, even `+feature/b:tmp-b` failed with
   `fatal: Refusing to fetch into current branch refs/heads/tmp-b of non-bare repository`
   -- fetch would move HEAD's branch under the working tree and index.
4. **`@{upstream}` vs. `@{push}`, `push.default`, ahead/behind counts:**
   `git switch -c work --track origin/main` printed "Branch 'work' set up to track remote
   branch 'main' from 'origin'" and `work@{upstream}` = `origin/main`.
   `work@{push}` depends on `push.default`:
   - `simple`: `fatal: cannot resolve 'simple' push to a single destination` -- simple
     refuses to push a branch to an upstream with a different name, so there is no
     answer (setting `remote.pushDefault=origin` did not change that).
   - `current`: `origin/work` -- push to the same name. Before `origin/work` existed,
     rev-parse failed with "unknown revision", because `@{push}` resolves to the
     remote-TRACKING ref, which only exists after a first push/fetch.
   - `upstream`: `origin/main`, i.e. the same as `@{u}`.
   After one local commit on `work` and one new commit on the server's main (+ fetch):
   `git branch -vv` showed `* work 758e7f7 [origin/main: ahead 1, behind 1] local work`
   (and `main ... [origin/main: behind 1]`), `git status -sb` showed
   `## work...origin/main [ahead 1, behind 1]`, and
   `git rev-list --left-right --count work@{u}...work` printed `1	1` (left = commits only
   in upstream, right = commits only in work).
   `.git/config` had
   `[branch "work"]` / `remote = origin` / `merge = refs/heads/main` -- note `merge` names
   the branch on the REMOTE side (`refs/heads/main`), not `refs/remotes/origin/main`.
   `git branch --unset-upstream` deleted both keys; afterwards `work@{u}` fails with
   `fatal: no upstream configured for branch 'work'`, `git status -sb` shows only
   `## work`, and `@{push}` under `current` no longer resolved either.

## WHAT SURPRISED ME

- Negative refspecs are global: `^refs/heads/review/*` also froze my
  `origin-review/*` mirror, not just the default namespace.
- `fetch --prune` does not prune tags; you need `--prune-tags` explicitly.
- `git log FETCH_HEAD` is only the first "for-merge" line, not everything fetched.
- `@{push}` names a remote-tracking ref, so it fails until that ref exists, and under
  `push.default=simple` it fails outright for a branch whose upstream has another name.
- Tag auto-following only picks up tags that point into history being fetched.

## ONE-LINE TAKEAWAY

A fetch refspec is "remote source : local destination", `+` allows forced mirroring,
fetch never deletes unless you `--prune` (and `--prune-tags` for tags), and a branch can
pull from `@{upstream}` while pushing to a different `@{push}` depending on
`push.default`.
