# Day 53, Task 8 -- Git: push refspecs, `push.default`, and deleting remote branches

## THE TASK

In a SCRATCH area (`/tmp/day53-lab`) create a bare repo to act as the remote (`git init --bare remote.git`), clone it twice (`alice/` and `bob/`), and make a couple of commits on `main` in `alice`. Work through the questions by actually running things -- never against a real remote.

1. In `alice`, create a local branch `wip-login` and push it so that on the remote it is called `feature/login` (one command, using a `src:dst` refspec). Then push only a specific older commit (by hash) to a new remote branch `snapshot`. What does `git ls-remote origin` show?
2. Compare `push.default` values `simple`, `current`, `upstream` and `matching`: set each in `alice` (local config only, scratch repo) and run a bare `git push` from a branch whose upstream has a DIFFERENT name than the local branch. Which values refuse, and which push where?
3. Delete the remote branch `snapshot` in two different ways (`git push origin --delete ...` and the empty-source refspec `:snapshot`). In `bob`, what does `git branch -r` still show until you run `git fetch --prune`? What does `fetch.prune` do?
4. What does a leading `+` in a refspec mean (e.g. `+wip-login:feature/login`), and how is it different from `--force` and from `--force-with-lease`? Show a case where `+` overwrote a commit `bob` had pushed.

## WHAT I RAN

```bash
mkdir -p /tmp/day53-lab && cd /tmp/day53-lab
git init --bare -b main remote.git
git clone remote.git alice && cd alice
git checkout -b main
echo one > f && git add f && git commit -m c1
echo two >> f && git commit -am c2
git push -u origin main
cd .. && git clone remote.git bob && cd alice

# 1. src:dst refspecs
git switch -c wip-login
echo l > login && git add login && git commit -m login
git push origin wip-login:feature/login
git push origin "$(git rev-parse --short main~1)":refs/heads/snapshot
git push origin "$(git rev-parse --short main~1)":snap2   # error: not a full refname
git ls-remote origin

# 2. push.default with an upstream of a DIFFERENT name
git branch --set-upstream-to=origin/feature/login
for m in simple current upstream matching; do
  git config push.default "$m"
  echo "$m" >> login && git commit -qam "$m"
  git push
done

# 3. deleting remote branches
(cd ../bob && git fetch && git branch -r)
git push origin --delete snapshot
git push origin :wip-login
cd ../bob
git branch -r            # still lists origin/snapshot and origin/wip-login
git fetch --prune        # - [deleted] (none) -> origin/snapshot / origin/wip-login
git branch -r

# 4. + vs --force vs --force-with-lease
git switch -c feature/login origin/feature/login
echo bob > bob && git add bob && git commit -m "bob work"
git push origin feature/login
cd ../alice && git config push.default simple
echo a2 >> login && git commit -am alice2
git push origin wip-login:feature/login        # ! [rejected] (fetch first)
git push origin +wip-login:feature/login       # + 741962c...e4ebc83 (forced update)
# alice fetches, bob pushes again afterwards; alice's tracking ref is now stale:
git push --force-with-lease origin wip-login:feature/login   # ! [rejected] (stale info)
```

## MY ANSWERS

1. `git push origin wip-login:feature/login` pushes the local branch `wip-login` to a remote
   branch named `feature/login` -- the part before the colon is the local source (any commit-ish),
   the part after is the remote destination ref. For a raw commit hash the destination has to be
   spelled out in full (`<hash>:refs/heads/snapshot`): with just `<hash>:snap2` git refuses with
   "The destination you provided is not a full refname", because it can't guess whether you
   wanted a branch or a tag when the source isn't a ref. `git ls-remote origin` then showed
   `HEAD`, `refs/heads/main`, `refs/heads/feature/login` (pointing at the `login` commit) and
   `refs/heads/snapshot` (pointing at `c1`, the older commit) -- there is no `wip-login` on the
   remote at all.
2. With `wip-login` tracking `origin/feature/login` and a bare `git push`:
   - `simple` (the default) **refuses**: "The upstream branch of your current branch does not
     match the name of your current branch". It only pushes when the names match.
   - `current` pushes to a branch with the **same name** as the local one, ignoring the upstream:
     it created a new remote branch `wip-login -> wip-login`.
   - `upstream` pushes to the configured **upstream**: `wip-login -> feature/login`.
   - `matching` pushes **every** local branch that has a same-named remote branch (here `main`
     -- nothing new -- and `wip-login`, which existed after the `current` push), so it updated
     `wip-login -> wip-login`, not the upstream. It is the dangerous old default, because it
     can push branches you weren't even on.
3. `git push origin --delete snapshot` and `git push origin :wip-login` (empty source = "push
   nothing into this ref" = delete) both remove the branch on the remote. `bob`, however, still
   listed `origin/snapshot` and `origin/wip-login` in `git branch -r`: remote-tracking refs are
   only local caches, and a plain `git fetch` never deletes them. `git fetch --prune` printed
   `- [deleted] (none) -> origin/snapshot` (and the same for `wip-login`) and removed them.
   `fetch.prune = true` (or `remote.<name>.prune`) makes every fetch/pull prune automatically.
4. A leading `+` in a refspec force-updates **that one ref** even when it is not a fast-forward;
   other refs in the same push stay protected. `--force` applies the same thing to every ref in
   the push. Neither checks what is on the remote: after bob pushed "bob work" (`741962c`) to
   `feature/login`, a normal push from alice was `! [rejected] (fetch first)`, but
   `git push origin +wip-login:feature/login` printed `+ 741962c...e4ebc83 (forced update)`
   and bob's commit vanished from the branch. `--force-with-lease` only forces if the remote
   ref still equals alice's remote-tracking ref (what she last saw); when bob pushed again
   after her fetch, it was rejected with `(stale info)` instead of silently destroying his work.
   (`--force-if-includes` adds a further check against a background `fetch` updating the
   tracking ref behind your back.)
