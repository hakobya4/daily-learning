# Day 24, Task 7 -- Git: `git notes`, `git describe`, `git archive`, `git log --merges`, `git commit --fixup=reword`

## THE TASK

In a SCRATCH repo (`/tmp/notes-lab`, `git init -b main`, a few commits, one tag, one merge):

1. How do you attach a note to an existing commit without changing its hash (`git notes add`), show it in `git log`, and why are notes not pushed by default?
2. What does `git describe --tags` print for a commit that is 3 commits after tag `v1.0`? What do the `-3-g<sha>` parts mean, and what do `--always` and `--dirty` add?
3. How do you export the tree of `HEAD` as a tarball without the `.git` folder (`git archive`), and how do you limit it to one subdirectory?
4. How do you list only merge commits, and only non-merge commits (`--merges`, `--no-merges`)? How do you see just the commits a merge brought in?
5. What does `git commit --fixup=reword:<sha>` do compared with a plain `--fixup=<sha>`, and how does `rebase -i --autosquash` use it?

## WHAT I RAN

```
git init -b main /tmp/notes-lab && cd /tmp/notes-lab
echo a > a.txt && git add . && git commit -m "first"
git tag v1.0
git notes add -m "reviewed by Ann" HEAD
git log -1                      # shows a "Notes:" section
git notes show HEAD
echo b > b.txt && git add . && git commit -m "second"
echo c > c.txt && git add . && git commit -m "third"
echo d > d.txt && git add . && git commit -m "fourth"
git describe --tags             # v1.0-3-g<sha>
git describe --tags --always --dirty
mkdir sub && echo x > sub/x.txt && git add . && git commit -m "sub"
git archive --format=tar.gz -o ../all.tar.gz HEAD
git archive --format=tar.gz -o ../sub.tar.gz HEAD sub
git switch -c feature && echo f > f.txt && git add . && git commit -m "feat"
git switch main && git merge --no-ff feature -m "merge feature"
git log --merges --oneline
git log --no-merges --oneline
git log --oneline HEAD^1..HEAD^2    # commits the merge brought in
git commit --allow-empty --fixup=reword:<sha>
git rebase -i --autosquash <sha>^
```

## MY ANSWERS

1. `git notes add -m "text" <commit>` stores the note in a separate ref (`refs/notes/commits`) that points at a blob, so the commit object and its hash never change. `git log` shows it under a "Notes:" heading by default, and `git notes show <commit>` prints it. Notes are not pushed or fetched by default because they live under `refs/notes/*`, and the default refspecs only cover `refs/heads/*` and tags; you have to push explicitly, e.g. `git push origin refs/notes/commits`, and fetch with `git fetch origin refs/notes/*:refs/notes/*`.
2. It prints `v1.0-3-g<abbrev-sha>`, e.g. `v1.0-3-g2a9c1f4`. `v1.0` is the nearest reachable tag, `3` is how many commits come after that tag, and `g` marks "git" followed by the abbreviated hash of the current commit. `--always` falls back to just the abbreviated sha when there is no tag to describe (instead of failing), and `--dirty` appends `-dirty` when the working tree has uncommitted changes to tracked files.
3. `git archive --format=tar.gz -o ../all.tar.gz HEAD` writes the tree of HEAD as a tarball; it contains only tracked files and no `.git` folder. Adding a path limits it, e.g. `git archive -o ../sub.tar.gz HEAD sub` (or `HEAD:sub` to make that directory the archive root). `--format=zip` works too.
4. `git log --merges` lists only commits with two or more parents; `git log --no-merges` lists only commits with one parent. To see the commits a merge brought in, use `git log <merge>^1..<merge>^2` (parent 2 minus what is reachable from parent 1), which lists exactly the commits on the merged branch that were not on the first parent's line.
5. A plain `--fixup=<sha>` creates a commit titled `fixup! <subject>` whose changes get squashed silently into the target commit during `rebase -i --autosquash`, keeping the target's message. `--fixup=reword:<sha>` creates an `amend!`-style commit whose message body replaces the target's message: it makes an (optionally empty) commit and lets you edit the new message, and autosquash then squashes it into the target and uses that new message (the rebase todo uses `fixup -C`, so the message is reworded). `--autosquash` reorders the todo list so each fixup/amend commit sits right after its target and changes the action to `fixup`/`fixup -C`.
