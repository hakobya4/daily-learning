# Day 31, Task 7 -- Git: `check-ignore`, `ls-files -o`, `archive`, `.gitattributes`, `assume-unchanged`

## THE TASK

In a SCRATCH repo (`/tmp/day31-lab`, `git init -b main`) with a `.gitignore` containing `*.log` and `build/`, a `.gitattributes`, and a few tracked + untracked files:

1. How do you find out WHICH rule in WHICH file ignores a path (`git check-ignore -v`)? What does it print for a path that is not ignored?
2. How do you list untracked files while respecting ignore rules (`git ls-files -o --exclude-standard`)? How do you list the ignored ones instead (`-i`)?
3. How do you export a clean snapshot of `HEAD` as a tarball without the `.git` directory (`git archive`)? How does `export-ignore` in `.gitattributes` change it?
4. What does `* text=auto` / `*.sh text eol=lf` in `.gitattributes` do, and why does it matter on a Windows + Linux team?
5. What do `git update-index --assume-unchanged` and `--skip-worktree` do, how do they differ from `.gitignore`, and how do you undo them (`git ls-files -v` shows them)?

## WHAT I RAN

```bash
rm -rf /tmp/day31-lab && mkdir /tmp/day31-lab && cd /tmp/day31-lab
git init -b main
printf '*.log\nbuild/\n' > .gitignore
printf '* text=auto\n*.sh text eol=lf\ndocs/ export-ignore\n' > .gitattributes
mkdir docs build && echo hi > app.txt && echo run > run.sh && echo d > docs/a.md
echo x > debug.log && echo y > build/out.bin && echo z > notes.txt
git add .gitignore .gitattributes app.txt run.sh docs && git commit -m init
git check-ignore -v debug.log build/out.bin app.txt   # app.txt prints nothing
git ls-files -o --exclude-standard
git ls-files -o -i --exclude-standard
git archive --format=tar.gz -o ../snap.tar.gz HEAD && tar tzf ../snap.tar.gz
git update-index --assume-unchanged app.txt
git update-index --skip-worktree run.sh
git ls-files -v           # h = assume-unchanged, S = skip-worktree
git update-index --no-assume-unchanged app.txt
git update-index --no-skip-worktree run.sh
```

## MY ANSWERS

1. `git check-ignore -v <path>` prints `source:linenumber:pattern<TAB>path`, e.g. `.gitignore:1:*.log	debug.log`, so you see which file and which line ignores it. For a path that is not ignored it prints nothing and exits with status 1 (0 means at least one path was ignored).
2. `git ls-files -o --exclude-standard` lists untracked files that are NOT ignored (here `notes.txt`). Adding `-i` (`git ls-files -o -i --exclude-standard`) flips it to list only the ignored untracked files (`debug.log`, `build/out.bin`).
3. `git archive --format=tar.gz -o snap.tar.gz HEAD` writes a tarball of the committed tree of HEAD only: no `.git`, no untracked or ignored files. Paths marked `export-ignore` in `.gitattributes` (e.g. `docs/ export-ignore`) are left out of the archive too, which is handy for dropping tests, docs or CI config from release tarballs.
4. `* text=auto` lets Git detect text files and normalise line endings to LF in the repository, converting to the platform's native ending on checkout. `*.sh text eol=lf` forces LF in the working tree for shell scripts, so a script checked out on Windows still has `\n` endings and does not break with `bad interpreter: /bin/bash^M` on Linux or in Docker. It also avoids whole-file diffs caused by CRLF/LF churn between teammates.
5. `--assume-unchanged` promises Git the file will not change, so Git skips checking it for modifications (a performance hint); `--skip-worktree` says "pretend my local version is the committed one", meant for local-only edits to tracked files such as config, and it survives pulls better (Git refuses to overwrite and makes you deal with it, whereas assume-unchanged can be silently reset). Both differ from `.gitignore`, which only affects UNTRACKED files; these two apply to files that are already tracked. `git ls-files -v` shows them: lowercase `h` = assume-unchanged, `S` = skip-worktree. Undo with `--no-assume-unchanged` / `--no-skip-worktree`.
