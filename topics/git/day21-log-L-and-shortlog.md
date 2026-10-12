# Day 21, Task 7 -- Git: `log -L`, `shortlog`, `cherry`, `merge-base --fork-point`

## THE TASK

In a SCRATCH repo (`/tmp/hist-lab`, `git init -b main`):

1. Create a file with a function in it, change that function in 3 separate commits (and change unrelated lines in 2 others). How do you list only the commits that touched that function's lines, with their diffs? (`git log -L`)
2. Make commits as two different authors (`git -c user.name=... -c user.email=... commit`). Which command summarises commits per author, and what does `-s -n` change?
3. Create `topic` from `main`, cherry-pick one of its commits onto `main`. What does `git cherry -v main topic` print for that commit versus the others, and why does it work without a shared hash?
4. Make `topic`, then rewrite `main` (e.g. `git commit --amend` an old tip after branching). What does `git merge-base --fork-point main topic` find that plain `git merge-base` does not, and which reflog entry does it rely on?
5. How would you attribute each line of a file to the commit that last changed it while ignoring whitespace-only changes and lines moved within the file (`blame` flags)?

## WHAT I RAN

```
mkdir /tmp/hist-lab && cd /tmp/hist-lab && git init -b main
git log -L :compute:app.py            # or -L 10,20:app.py
git shortlog -sn                      # summary, sorted by count
git switch -c topic main
git cherry-pick <sha>                 # onto main
git cherry -v main topic
git commit --amend                    # on main after branching
git merge-base --fork-point main topic
git blame -w -M -C file.txt
```

## MY ANSWERS

1. `git log -L :funcname:file` (or `-L start,end:file`) walks history and shows only the commits that touched those lines, each with the diff restricted to that range. Git follows the function as it moves, so the 2 unrelated commits are skipped.
2. `git shortlog` groups commits by author with their subjects. `-s` suppresses the subjects and prints only a count per author; `-n` sorts by number of commits (descending) instead of alphabetically. So `git shortlog -sn` is a leaderboard.
3. `git cherry -v main topic` lists commits on `topic` not in `main`. A commit already applied to `main` is prefixed with `-`; the others get `+`. It works without a shared hash because it compares patch-ids (a hash of the diff itself, ignoring line numbers and whitespace), and a cherry-pick produces a different commit hash but the same patch.
4. If `main` is rewritten after `topic` branched (amend, rebase), plain `git merge-base main topic` uses only the current commit graph and may return an old ancestor or the wrong base. `--fork-point` also consults the reflog of `main` (`refs/heads/main` reflog, i.e. `main@{n}`) to find where `topic` really forked from the earlier tips of `main`, so you get the correct base for rebasing. It needs the reflog entries to still exist (not expired or gc'd).
5. `git blame -w -M -C file`: `-w` ignores whitespace-only changes, `-M` detects lines moved within the file, and `-C` detects lines copied/moved from other files (repeat `-C` for more aggressive searching). `--ignore-rev <sha>` or `--ignore-revs-file` can also skip specific formatting commits.
