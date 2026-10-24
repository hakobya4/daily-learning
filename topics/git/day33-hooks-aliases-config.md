# Day 33, Task 8 -- Git: hooks, aliases, and layered config

## THE TASK

In a SCRATCH repo (`/tmp/day33-lab`, `git init -b main`):

1. Where do the three config levels live (`--system`, `--global`, `--local`), which wins when they disagree, and how do you see where a value comes from (`git config --show-origin --get-all ...`)?
2. How do you create an alias `git lg` that shows a one-line graph log of all branches, and an alias that runs an external shell command (the `!` prefix)?
3. What does a `pre-commit` hook do, where does it live, what must be true for it to run, and how do you make a commit that rejects any staged file containing the text `TODO-REMOVE`? How do you bypass it once (`--no-verify`)?
4. Why are hooks in `.git/hooks` not shared through clone, and how does `core.hooksPath` let a team share them from the repo?
5. What does `includeIf "gitdir:..."` in the global config let you do (for example a different `user.email` for work repos)?

## WHAT I RAN

```bash
rm -rf /tmp/day33-lab && mkdir /tmp/day33-lab && cd /tmp/day33-lab
git init -b main
git config --show-origin --get-all user.email          # which file each value comes from
git config --local user.email "lab@example.com"        # local overrides global overrides system
git config --local alias.lg "log --oneline --graph --decorate --all"
git config --local alias.root '!pwd'                   # '!' = run as a shell command
git lg
cat > .git/hooks/pre-commit <<'HOOK'
#!/bin/sh
if git diff --cached -U0 | grep -q 'TODO-REMOVE'; then
    echo "pre-commit: staged changes contain TODO-REMOVE" >&2
    exit 1
fi
HOOK
chmod +x .git/hooks/pre-commit
echo 'TODO-REMOVE this' > a.txt && git add a.txt && git commit -m "x"   # rejected
git commit --no-verify -m "x"                                          # bypass once
mkdir .githooks && git config core.hooksPath .githooks                 # shareable hooks dir
```

## MY ANSWERS

1. Three levels: `--system` (`/etc/gitconfig`, all users), `--global` (`~/.gitconfig` or `~/.config/git/config`, one user) and `--local` (`.git/config`, one repo). The more specific level wins: local over global over system. `git config --show-origin --get-all <key>` prints every value and the file it came from; `git config --list --show-origin` shows everything.
2. `git config --global alias.lg "log --oneline --graph --decorate --all"` makes `git lg` a one-line graph of all branches. An alias starting with `!` is run by the shell instead of as a git subcommand, e.g. `git config alias.root '!pwd'` or `'!git fetch -p && git log ...'`; it runs from the repo's top-level directory.
3. `pre-commit` is a script that git runs before creating a commit, after `git commit` is invoked and before the message editor opens. It lives at `.git/hooks/pre-commit` and must be executable (no `.sample` suffix). If it exits non-zero, the commit is aborted. For `TODO-REMOVE`, the hook runs `git diff --cached -U0 | grep -q TODO-REMOVE` and exits 1 when found. `git commit --no-verify` (`-n`) skips pre-commit and commit-msg hooks for that one commit.
4. `.git` is not part of the committed content, so it is never cloned; hooks there stay local. Putting hooks in a tracked folder (e.g. `.githooks/`) and running `git config core.hooksPath .githooks` makes git use that folder. The setting itself is local config, so each developer runs it once (often via a setup script or `make`).
5. `[includeIf "gitdir:~/work/"]` with `path = ~/.gitconfig-work` in the global config loads extra config only for repos under that directory, so work repos can use a different `user.email`/signing key while personal repos keep the default. The trailing slash matches everything below it; `gitdir/i` ignores case.
