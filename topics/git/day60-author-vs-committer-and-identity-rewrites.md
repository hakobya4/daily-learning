# Day 60, Task 8 -- Git: author vs. committer, one-off identities (`-c`, `--author`, `GIT_*` env), and fixing the wrong identity in history

## THE TASK

In a SCRATCH repo (`/tmp/day60-lab`, `git init -b main`) make 3 commits with your normal identity, then 2 commits on purpose with a WRONG identity (for example `Bot <bot@example.invalid>`), then 1 more normal commit. Answer the questions by actually running the commands -- never rewrite a real project's history, and never touch your global config for this lab.

1. Every commit stores TWO identities. Show them side by side with `git log --format='%h  A:%an <%ae> %ad  C:%cn <%ce> %cd' --date=iso`. When do the author and the committer differ in real life? Produce a commit where they differ by using `git commit --author="Someone <someone@example.invalid>"`, and another by `git cherry-pick`-ing or `git rebase`-ing an older commit -- which fields changed and which were kept?
2. Make one commit with a ONE-OFF identity in three different ways and confirm afterwards that `.git/config` and `git config --get user.email` are unchanged each time: (a) `git -c user.name=... -c user.email=... commit ...`, (b) the environment variables `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_NAME` / `GIT_COMMITTER_EMAIL` on a single command line, (c) `git commit --author=...` -- what does (c) NOT change? Then show why `git config user.email ...` (without `--global`) is the dangerous option for automation: which file does it write, and which LATER commits does it silently affect?
3. Fix the 2 wrong-identity commits. First with `git rebase -i <base>` + `exec git commit --amend --no-edit --reset-author` (or `git rebase --exec ... `) -- what does `--reset-author` reset besides the name and email (look at the author date)? Then reset the lab and do it again with `git filter-branch --env-filter` that only rewrites commits whose `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_EMAIL` is the bot address (and read the warning filter-branch prints -- what does the git documentation recommend instead, and what would the equivalent `git filter-repo --mailmap` / `--email-callback` call look like?). Compare the commit hashes before and after: which ones changed and why did EVERY later commit change too?
4. After a rewrite like that has been pushed: what does `git push --force-with-lease` protect you from that `--force` does not, what must every other clone do (`git fetch` + `git reset --hard origin/main`, or `git rebase --onto`), and where does `refs/original/` (left by filter-branch) or the reflog still keep the old commits? How is fixing the history different from just adding a `.mailmap` entry (day 40), which never rewrites anything?

## WHAT I RAN

```bash
# Build the lab history (3 normal, 2 wrong-identity, 1 normal commit).
# GIT_CONFIG_GLOBAL=/dev/null keeps my real ~/.gitconfig out of the experiment.
mkdir /tmp/day60-lab && cd /tmp/day60-lab && git init -q -b main
export GIT_CONFIG_GLOBAL=/dev/null
me='-c user.name=Narek -c user.email=narek@example.invalid'
bot='-c user.name=Bot -c user.email=bot@example.invalid'
c(){ id="$1"; shift; echo "$*" >> f.txt; git add f.txt; git $id commit -qm "$*"; sleep 1; }
c "$me" one; c "$me" two; c "$me" three; c "$bot" four; c "$bot" five; c "$me" six

# Q1: author vs committer, --author, cherry-pick / rebase
git log --format='%h  A:%an <%ae> %ad  C:%cn <%ce> %cd' --date=iso
echo x > g; git add g
git $me commit -q --author="Someone <someone@example.invalid>" -m other
git log -1 --format='%h  A:%an <%ae> %ad  C:%cn <%ce> %cd' --date=iso
# cherry-pick (separate tiny repo): Someone commits on feat, Narek picks it onto main 2s later
git checkout -q -b feat; echo x > a; git add a
git -c user.name=Someone -c user.email=someone@example.invalid commit -qm feature
sleep 2; git checkout -q main; git $me cherry-pick feat
git log --all --format='%h %s  A:%ae %ad  C:%ce %cd' --date=iso

# Q2: -c, GIT_* env vars, --author; then the `git config user.email` trap
git $me commit -q --allow-empty -m via-dash-c            # (a)
GIT_AUTHOR_NAME=Env GIT_AUTHOR_EMAIL=env@example.invalid \
GIT_COMMITTER_NAME=Env GIT_COMMITTER_EMAIL=env@example.invalid \
  git commit -q --allow-empty -m via-env                 # (b)
git $me commit -q --allow-empty --author="Other <other@example.invalid>" -m via-author  # (c)
git log -3 --format='%h A:%ae C:%ce %s'
git config --get user.email; echo "exit=$?"              # nothing set -> exit 1
cat .git/config                                          # no [user] section
git config user.email bot@example.invalid; git config user.name Bot   # the trap
tail -3 .git/config
git commit -q --allow-empty -m "later human commit"; git log -1 --format='%h A:%ae C:%ce'
git config --unset user.email; git config --unset user.name           # undo

# Q3: rebase --exec --reset-author; filter-branch --env-filter (and the filter-repo equivalent)
cp -r /tmp/day60-lab /tmp/day60-lab2                     # keep a copy for filter-branch
git log --format='%h %ae %s'                             # BEFORE
git $me rebase -q HEAD~5 --exec \
  'git -c user.name=Narek -c user.email=narek@example.invalid commit -q --amend --no-edit --reset-author'
git log --format='%h A:%ae %ad C:%ce' --date=iso         # AFTER (rebase)

cd /tmp/day60-lab2
git filter-branch --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "bot@example.invalid" ]; then
  export GIT_AUTHOR_NAME=Narek GIT_AUTHOR_EMAIL=narek@example.invalid
fi
if [ "$GIT_COMMITTER_EMAIL" = "bot@example.invalid" ]; then
  export GIT_COMMITTER_NAME=Narek GIT_COMMITTER_EMAIL=narek@example.invalid
fi' -- --all
git log --format='%h %ae %ad %ce %s' --date=iso          # AFTER (filter-branch)
git for-each-ref refs/original

# filter-repo equivalent (not installed here; what I would run):
#   printf 'Narek <narek@example.invalid> Bot <bot@example.invalid>\n' > /tmp/mailmap
#   git filter-repo --mailmap /tmp/mailmap
# or
#   git filter-repo --email-callback '
#     return b"narek@example.invalid" if email == b"bot@example.invalid" else email'

# Q4: force-with-lease, other clones, refs/original and reflog
# (only reasoned about / read docs -- this lab has no remote)
#   git push --force-with-lease=main:<old-sha> origin main
#   other clone: git fetch && git reset --hard origin/main
#        or keep local work: git rebase --onto origin/main <old-upstream-sha> my-branch
#   git reflog main ; git for-each-ref refs/original
```

## ANSWERS

1. **Author vs. committer (paste the log lines):**
   ```
   fbb6f0a  A:Narek <narek@example.invalid> 2026-11-20 04:59:09 +0000  C:Narek <narek@example.invalid> 2026-11-20 04:59:09 +0000
   524c569  A:Bot <bot@example.invalid> 2026-11-20 04:59:08 +0000  C:Bot <bot@example.invalid> 2026-11-20 04:59:08 +0000
   97ce3e6  A:Bot <bot@example.invalid> 2026-11-20 04:59:07 +0000  C:Bot <bot@example.invalid> 2026-11-20 04:59:07 +0000
   a15df32  A:Narek <narek@example.invalid> 2026-11-20 04:59:06 +0000  C:Narek <narek@example.invalid> 2026-11-20 04:59:06 +0000
   ...
   # --author:
   b7d4c72  A:Someone <someone@example.invalid> 2026-11-20 04:59:10 +0000  C:Narek <narek@example.invalid> 2026-11-20 04:59:10 +0000
   # cherry-pick: original vs. picked copy
   40769af feature  A:someone@example.invalid 2026-11-20 04:59:39 +0000  C:someone@example.invalid 2026-11-20 04:59:39 +0000
   544b27c feature  A:someone@example.invalid 2026-11-20 04:59:39 +0000  C:narek@example.invalid 2026-11-20 04:59:41 +0000
   ```
   The **author** is whoever wrote the change (and when they first wrote it); the **committer** is whoever last
   created *this particular commit object* (and when). For a fresh commit they are the same. They differ when
   someone applies another person's work: `git am` of an emailed patch, a maintainer cherry-picking a contributor's
   fix, `git rebase` / `commit --amend` of somebody else's commit, or `--author=` when committing for a pair partner.
   In the cherry-pick above the author name, email **and date** were kept (`04:59:39`), while the committer became
   me with the new time (`04:59:41`) -- and because the committer changed, the hash changed (`40769af` -> `544b27c`).
   Rebase behaves the same way: it re-creates every replayed commit, keeping author info and resetting the committer.
   GitHub's contribution graph counts the **author** email (it must be linked to the account).

2. **One-off identities and the `git config user.email` trap:**
   - (a) `git -c user.name=X -c user.email=Y commit` sets the config value only for that one process: both author
     and committer become X/Y, nothing is written to disk.
   - (b) `GIT_AUTHOR_NAME/EMAIL` and `GIT_COMMITTER_NAME/EMAIL` on the same command line override config (they win
     over `user.*`), again only for that process: `49c7619 A:env@example.invalid C:env@example.invalid`.
     (`GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` exist too.)
   - (c) `--author="Other <other@...>"` changes **only the author**; the committer still comes from config:
     `9866bc8 A:other@example.invalid C:narek@example.invalid`.
   - After all three, `git config --get user.email` still printed nothing (exit 1) and `.git/config` had no
     `[user]` section.
   - The trap: `git config user.email bot@...` (no `--global`) writes a `[user]` section into the repo's
     **`.git/config`** and it stays there. Every LATER commit in that repo by anyone -- including the human's own
     commits from the editor -- is now silently `A:bot C:bot` (`74ca812 A:bot@example.invalid C:bot@example.invalid`),
     because repo-local config beats `~/.gitconfig`. For automation, always use (a) or (b) scoped to the single
     command, and if you find a leftover, `git config --unset user.email` / `--unset user.name`.

3. **Rewriting the wrong commits (rebase --exec vs. filter-branch --env-filter):**
   ```
   BEFORE                       rebase --exec --reset-author     filter-branch --env-filter (bot only)
   b7d4c72 other  (Someone)     4e60309  A:narek 04:59:11        36c3d69  A:someone (kept) 04:59:10
   fbb6f0a six                  a4aa55a  A:narek 04:59:11        995f2d3                   04:59:09
   524c569 five   (Bot)         3d06e5f  A:narek 04:59:11        1c8cc8d  A:narek          04:59:08
   97ce3e6 four   (Bot)         91fa06a  A:narek 04:59:11        fe9bebb  A:narek          04:59:07
   a15df32 three                e036655  A:narek 04:59:11        a15df32  (unchanged)
   2a547c8 two                  2a547c8  (unchanged)             2a547c8  (unchanged)
   4a701aa one                  4a701aa  (unchanged)             4a701aa  (unchanged)
   ```
   - `--reset-author` makes *me* the author **and resets the author date to now** -- every replayed commit got
     `04:59:11`, so the original timestamps were lost. Also note `--exec` ran on *every* commit after the base, so
     it even rewrote `three` and stole `other` from Someone; a careful version uses `rebase -i` and puts `exec` only
     after the bot commits, or uses a conditional filter as below.
   - `filter-branch --env-filter` with the `if` checks only touched the bot fields and kept the original dates.
     `three` and earlier kept their hashes because nothing about them changed.
   - Every commit **after** the first rewritten one changed too, even though its own content/identity did not
     (`six`, `other`): a commit hash covers its parent's hash, so a new parent means a new hash, all the way to the tip.
   - filter-branch prints a warning recommending **`git filter-repo`** (faster, safer, no `refs/original` mess).
     Equivalent: put `Narek <narek@example.invalid> Bot <bot@example.invalid>` in a mailmap file and run
     `git filter-repo --mailmap that-file`, or
     `git filter-repo --email-callback 'return b"narek@example.invalid" if email == b"bot@example.invalid" else email'`.

4. **After the rewrite: force-with-lease, other clones, where the old commits still live:**
   - A rewritten branch no longer fast-forwards from the remote, so it needs a forced push.
     `--force` overwrites whatever is on the remote; `--force-with-lease` (ideally `--force-with-lease=main:<sha I
     expect>`) refuses if the remote branch has moved since I last fetched it, so I can't silently destroy a
     commit somebody else pushed in the meantime.
   - Every other clone still has the old commits. With no local work: `git fetch && git reset --hard origin/main`.
     With local commits on top of the old history: `git rebase --onto origin/main <old-upstream-sha> my-branch`
     (a plain `git pull` would merge the old and new histories and bring the bad commits back).
   - The old commits are not gone yet: filter-branch keeps the old tip in `refs/original/refs/heads/main`
     (`b7d4c72` above), and the reflog (`git reflog main`, `ORIG_HEAD`) still points at them until it expires and
     `git gc` prunes them; on GitHub old SHAs can stay reachable by URL for a while. Delete `refs/original` with
     `git update-ref -d` once the rewrite is verified.
   - A `.mailmap` entry (day 40) is the opposite approach: it only changes how `log`/`shortlog`/`blame` *display*
     names, never touches a commit, so no hashes change and nobody has to force-push or re-clone -- but the wrong
     email is still stored in the commits (and GitHub ignores `.mailmap` for contribution credit). Rewriting
     actually fixes the data at the cost of new hashes for everyone.

## ONE-LINE TAKEAWAY

Author = who wrote it, committer = who made this commit object; set identity per command with `-c` or `GIT_*` env (never repo-local `git config user.*` in automation), and remember any identity rewrite changes every later hash and needs `--force-with-lease` plus a reset in every clone.
