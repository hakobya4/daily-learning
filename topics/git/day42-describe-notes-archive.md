# Day 42, Task 7 -- Git: describe, notes and archive

## THE TASK

In a SCRATCH area (`/tmp/day42-lab`) create a repo with a few commits and an
annotated tag `v1.0` on the first one.

1. What does `git describe` print for a commit 3 commits after `v1.0`? Explain each part of `v1.0-3-g<hash>`. How do `--tags`, `--always` and `--dirty` change it?
2. Difference between a lightweight and an annotated tag; which one does `git describe` use by default?
3. `git notes add -m "reviewed" <commit>`: where are notes stored, why do they not change the commit hash, and why are they not pushed by default? Give the command to push them.
4. `git archive --format=tar.gz -o out.tgz HEAD` -- what is included/excluded compared to copying the working folder? How does `.gitattributes` `export-ignore` affect it?
5. How do you list commits reachable from `v1.0` but not from `main` (two dot notation vs three dots)?

## WHAT I RAN

```bash
mkdir /tmp/day42-lab && cd /tmp/day42-lab && git init -b main
# 4 commits c1..c4, annotated tag on the first:
git tag -a v1.0 -m rel          # right after c1
git describe                    # v1.0-3-g7b46d24
git describe --always --dirty   # same when clean; -dirty appended after editing a tracked file
git tag light HEAD              # lightweight tag on HEAD
git describe                    # still v1.0-3-g7b46d24 (ignores lightweight tags)
git describe --tags             # light
git notes add -m reviewed HEAD
git for-each-ref refs/notes     # refs/notes/commits
git checkout -b side v1.0 && echo s > s && git add s && git commit -m side && git checkout main
git log --oneline main..side    # 1 commit (side)
git log --oneline side..main    # 3 commits
git log --oneline main...side   # 4 commits (symmetric difference)
echo 'f export-ignore' > .gitattributes && git add .gitattributes && git commit -m ga
git archive --format=tar.gz -o /tmp/out.tgz HEAD && tar tzf /tmp/out.tgz   # only .gitattributes; f is gone
```

## MY ANSWERS

1. `v1.0-3-g7b46d24` = nearest reachable annotated tag (`v1.0`), `3` commits on top of it, `g` + abbreviated hash of the commit being described (the `g` just says "git"). `--tags` also considers lightweight tags (so `light` on HEAD wins and prints just `light`). `--always` falls back to a bare abbreviated hash when no tag is reachable instead of failing. `--dirty` appends `-dirty` if the working tree has uncommitted changes to tracked files.
2. A lightweight tag is just a ref pointing at a commit. An annotated tag is a real object with tagger, date, message (and optional signature) that points at the commit. `git describe` only uses annotated tags by default; lightweight ones need `--tags`.
3. Notes live in their own ref, `refs/notes/commits`, as a separate tree mapping commit hash -> note blob. The commit object is untouched, so its hash does not change. They are not pushed or fetched by default because only `refs/heads` and `refs/tags` have default refspecs. Push with `git push origin refs/notes/commits` (fetch with `git fetch origin refs/notes/commits:refs/notes/commits`).
4. `git archive` packs only the tracked content of the given tree (`HEAD`): no `.git` directory, no untracked or ignored files, no uncommitted edits, and it records the commit id in the tar header. A plain copy of the folder includes all of that. Paths marked `export-ignore` in `.gitattributes` are also left out (in my lab the archive contained only `.gitattributes`, because `f` was export-ignored); `export-subst` can expand placeholders such as `$Format:%H$`.
5. `git log main..side` = commits reachable from `side` but not from `main` (for the task, `git log main..v1.0` / `v1.0..main` depending on direction: `A..B` is "in B not in A"). Three dots, `main...side`, is the symmetric difference: commits reachable from either but not both. In the lab: `main..side` 1, `side..main` 3, `main...side` 4.
