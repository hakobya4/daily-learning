# Day 60, Task 8 -- Git: author vs. committer, one-off identities (`-c`, `--author`, `GIT_*` env), and fixing the wrong identity in history

## THE TASK

In a SCRATCH repo (`/tmp/day60-lab`, `git init -b main`) make 3 commits with your normal identity, then 2 commits on purpose with a WRONG identity (for example `Bot <bot@example.invalid>`), then 1 more normal commit. Answer the questions by actually running the commands -- never rewrite a real project's history, and never touch your global config for this lab.

1. Every commit stores TWO identities. Show them side by side with `git log --format='%h  A:%an <%ae> %ad  C:%cn <%ce> %cd' --date=iso`. When do the author and the committer differ in real life? Produce a commit where they differ by using `git commit --author="Someone <someone@example.invalid>"`, and another by `git cherry-pick`-ing or `git rebase`-ing an older commit -- which fields changed and which were kept?
2. Make one commit with a ONE-OFF identity in three different ways and confirm afterwards that `.git/config` and `git config --get user.email` are unchanged each time: (a) `git -c user.name=... -c user.email=... commit ...`, (b) the environment variables `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_NAME` / `GIT_COMMITTER_EMAIL` on a single command line, (c) `git commit --author=...` -- what does (c) NOT change? Then show why `git config user.email ...` (without `--global`) is the dangerous option for automation: which file does it write, and which LATER commits does it silently affect?
3. Fix the 2 wrong-identity commits. First with `git rebase -i <base>` + `exec git commit --amend --no-edit --reset-author` (or `git rebase --exec ... `) -- what does `--reset-author` reset besides the name and email (look at the author date)? Then reset the lab and do it again with `git filter-branch --env-filter` that only rewrites commits whose `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_EMAIL` is the bot address (and read the warning filter-branch prints -- what does the git documentation recommend instead, and what would the equivalent `git filter-repo --mailmap` / `--email-callback` call look like?). Compare the commit hashes before and after: which ones changed and why did EVERY later commit change too?
4. After a rewrite like that has been pushed: what does `git push --force-with-lease` protect you from that `--force` does not, what must every other clone do (`git fetch` + `git reset --hard origin/main`, or `git rebase --onto`), and where does `refs/original/` (left by filter-branch) or the reflog still keep the old commits? How is fixing the history different from just adding a `.mailmap` entry (day 40), which never rewrites anything?

## WHAT I RAN

```bash
# TODO: build the lab history (3 normal, 2 wrong-identity, 1 normal commit)


# Q1: author vs committer, --author, cherry-pick / rebase


# Q2: -c, GIT_* env vars, --author; then the `git config user.email` trap


# Q3: rebase --exec --reset-author; filter-branch --env-filter (and the filter-repo equivalent)


# Q4: force-with-lease, other clones, refs/original and reflog
```

## ANSWERS

1. **Author vs. committer (paste the log lines):**
   ```
   TODO: paste the side-by-side log output
   ```
   TODO: when they differ, and what cherry-pick / rebase changed vs. kept

2. **One-off identities and the `git config user.email` trap:**
   TODO

3. **Rewriting the wrong commits (rebase --exec vs. filter-branch --env-filter):**
   ```
   TODO: hashes before / after
   ```
   TODO: what --reset-author resets, why later hashes change, what filter-repo would look like

4. **After the rewrite: force-with-lease, other clones, where the old commits still live:**
   TODO

## ONE-LINE TAKEAWAY

TODO
