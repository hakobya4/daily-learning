# Day 55, Task 8 -- Git: `.gitattributes` merge drivers, `check-attr` and `merge-tree`

## THE TASK

In a SCRATCH repo (`/tmp/day55-lab`, `git init`, a couple of branches that edit the same files) explore how attributes change merge behaviour. Work through the questions by actually running things -- never in a real project's history.

1. Create a `CHANGELOG.md` that two branches both append a line to at the end, and merge them -- you get a conflict. Now add `CHANGELOG.md merge=union` to `.gitattributes`, redo the merge (reset first), and show the result. What does the built-in `union` driver do with the two sides, and why is it dangerous for files where order or uniqueness matters (e.g. a JSON file)?
2. Mark a generated file (e.g. `package-lock.json` or a fake `build/version.txt`) with `merge=ours`. Merge a branch that changed it. Does `merge=ours` do anything on its own? What extra config does it need (`git config merge.ours.driver true`), and how is this different from `git merge -s ours` and from `-X ours`?
3. Write a tiny custom merge driver in the scratch repo's LOCAL config (`merge.<name>.name` / `merge.<name>.driver` using the `%O %A %B %P` placeholders -- e.g. a script that keeps the numerically larger value in `VERSION`). Which file must the driver write its result to, and what must its exit status be to signal a conflict?
4. Use `git check-attr -a <path>` and `git check-attr merge -- <paths>` to show which attributes apply, including one inherited from a pattern in a subdirectory's `.gitattributes`. Then use `git merge-tree --write-tree <branch1> <branch2>` (Git >= 2.38) to compute a merge WITHOUT touching the working tree or index: what does it print on a clean merge vs. a conflicting one, and what is its exit code in each case?

## WHAT I RAN

```bash
mkdir /tmp/day55-lab && cd /tmp/day55-lab
git init -b main
git config user.name Narek; git config user.email narek@example.com
printf '# Changelog\n- initial\n' > CHANGELOG.md
mkdir build; echo 1.0 > build/version.txt; echo 3 > VERSION
git add .; git commit -m init

# two branches editing the same three files
git switch -c feature
echo '- feature line' >> CHANGELOG.md; echo 2.0-feature > build/version.txt; echo 7 > VERSION
git commit -am feature
git switch main
echo '- main line' >> CHANGELOG.md; echo 1.1-main > build/version.txt; echo 5 > VERSION
git commit -am main

# Q1: plain merge -> CONFLICT in all three files (exit 1)
git merge feature; git diff --name-only --diff-filter=U; git merge --abort
echo 'CHANGELOG.md merge=union' > .gitattributes
git add .gitattributes; git commit -m attrs
git merge feature            # CHANGELOG.md now auto-merges, the other two still conflict
cat CHANGELOG.md             # initial / main line / feature line -- no markers
git merge --abort

# Q2: merge=ours without and with the driver config
echo 'build/version.txt merge=ours' >> .gitattributes; git commit -am "ours attr"
git merge feature; git diff --name-only --diff-filter=U   # build/version.txt STILL conflicts
git merge --abort
git config merge.ours.driver true
git merge feature; git diff --name-only --diff-filter=U   # now only VERSION conflicts
cat build/version.txt                                     # 1.1-main (our side kept)
git merge --abort

# Q3: custom driver -- keep the numerically larger VERSION
mkdir -p .git/drivers
cat > .git/drivers/maxver.sh <<'EOF'
#!/bin/sh
# %O=ancestor %A=ours (result goes HERE) %B=theirs %P=path
a=$(cat "$2"); b=$(cat "$3")
case "$a$b" in *[!0-9]*) exit 1 ;; esac     # non-numeric -> report a conflict
[ "$b" -gt "$a" ] && printf '%s\n' "$b" > "$2"
exit 0
EOF
chmod +x .git/drivers/maxver.sh
git config merge.maxver.name "keep the numerically larger VERSION"
git config merge.maxver.driver '.git/drivers/maxver.sh %O %A %B %P'
echo 'VERSION merge=maxver' >> .gitattributes; git commit -am "maxver attr"
git merge --no-edit feature  # exit 0, clean merge commit
cat VERSION build/version.txt CHANGELOG.md   # 7 / 1.1-main / both changelog lines

# Q4: check-attr, including a pattern from a subdirectory's .gitattributes
mkdir -p docs/gen; echo '*.txt merge=union text' > docs/.gitattributes
echo x > docs/gen/a.txt; echo y > docs/readme.md; git add docs; git commit -m docs
git check-attr -a docs/gen/a.txt
git check-attr merge -- CHANGELOG.md VERSION build/version.txt docs/gen/a.txt docs/readme.md

# merge-tree --write-tree (needs git >= 2.38; my laptop has 2.34, so I ran this part
# with git 2.43) -- computes the merge without touching worktree or index
git switch -c clean1 main~2; echo a > only-a.txt; git add only-a.txt; git commit -m a
git switch -c clean2 main~2; echo b > only-b.txt; git add only-b.txt; git commit -m b
git merge-tree --write-tree clean1 clean2; echo "exit=$?"
git switch -c c1 main~2; echo one > clash.txt; git add clash.txt; git commit -m c1
git switch -c c2 main~2; echo two > clash.txt; git add clash.txt; git commit -m c2
git merge-tree --write-tree c1 c2; echo "exit=$?"
git merge-tree --write-tree --name-only c1 c2
git status --short            # empty: nothing in the worktree/index changed
```

## MY ANSWERS

1. Without attributes, both branches appending a line at the same spot is a normal content conflict (`CONFLICT (content): Merge conflict in CHANGELOG.md`, exit 1). With `CHANGELOG.md merge=union` the built-in `union` driver does a 3-way merge but, for every conflicting hunk, simply keeps the lines from BOTH sides (ours first, then theirs) and writes no conflict markers -- my file came out as `- initial`, `- main line`, `- feature line` and the merge reported no conflict for it. That is great for append-only, order-insensitive line lists, but dangerous anywhere structure, order or uniqueness matters: in JSON you can get two values for the same key, a missing/extra comma or two closing braces (invalid file), in a list of unique IDs you get duplicates, and if both sides *changed the same line* you silently get both the old-ish and new versions next to each other. Git never warns you, so the bug only shows up later.
2. On its own, `build/version.txt merge=ours` did nothing useful: `ours` is NOT a built-in merge driver name (built-ins are `text`, `binary`, `union`), so git treats it as an undefined driver and falls back to the normal text merge -- I still got `CONFLICT (content)` in `build/version.txt`. After `git config merge.ours.driver true` it works: the driver command `true` leaves `%A` (our version) untouched and exits 0, so git records "merged cleanly, result = ours" for that ONE file; `build/version.txt` stayed `1.1-main`. Differences: `git merge -s ours` is a whole-merge *strategy* that ignores the other branch's tree completely (every file stays as ours, the branch is only recorded as a parent). `-X ours` is an option to the default `ort` strategy that resolves only the *conflicting hunks* in our favour, in every file, while non-conflicting changes from the other side still come in. The `merge=ours` attribute is per-path and keeps our whole file for that path, conflict or not -- but only when both sides changed it (if only the other side changed it, git just takes their version without calling any driver).
3. The driver is configured in the repo's local config (`merge.maxver.name` is just a description; `merge.maxver.driver` is the command) and selected with `VERSION merge=maxver` in `.gitattributes`. Git writes the three versions to temp files and substitutes `%O` (ancestor), `%A` (ours), `%B` (theirs) and `%P` (the real path, for messages). The driver must write the merged result INTO the `%A` file -- git reads it back from there. Exit status 0 means "merged cleanly"; any non-zero exit means "conflict", and git then leaves whatever is in `%A` in the work tree and marks the path unmerged. My script kept `7` (the larger of main's `5` and feature's `7`) and exits 1 if either side is not a plain number. Because the driver lives in `.git/config` and `.git/drivers/`, it is NOT shared by cloning -- everyone has to configure it themselves (the `.gitattributes` line alone is harmless but then behaves like q2's undefined driver).
4. `git check-attr -a docs/gen/a.txt` printed `merge: union` and `text: set` -- both come from `docs/.gitattributes` (`*.txt merge=union text`), whose patterns apply relative to `docs/` and to everything below it, so the file in `docs/gen/` inherits them. `git check-attr merge -- ...` showed `CHANGELOG.md: merge: union`, `VERSION: merge: maxver`, `build/version.txt: merge: ours`, `docs/gen/a.txt: merge: union` and `docs/readme.md: merge: unspecified` (no pattern matched). `git merge-tree --write-tree A B` does a real `ort` merge purely in the object database: on a clean merge it prints just the OID of the resulting top-level tree (`86234026...`) and exits 0; on a conflict it exits 1 and prints the tree OID (that tree contains the files WITH conflict markers), then the "conflicted file info" lines `<mode> <object> <stage>\t<path>` (stages 2 and 3 for my add/add `clash.txt`), a blank line, and the informational messages (`Auto-merging clash.txt`, `CONFLICT (add/add): ...`). `--name-only` shrinks the conflicted section to just the paths. My `git status` stayed empty, so it is safe for "would this PR merge?" checks on a server or in a bare repo; you can then turn a clean result into a commit with `git commit-tree <tree> -p A -p B`. (Exit codes other than 0/1 mean an actual error. My laptop's git 2.34 doesn't have `--write-tree` yet; it needs 2.38+.)
