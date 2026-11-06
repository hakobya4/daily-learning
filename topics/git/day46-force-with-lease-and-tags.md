# Day 46, Task 7 -- Git: force-with-lease, annotated vs lightweight tags

## THE TASK

In a SCRATCH area (`/tmp/day46-lab`) create a bare repo `origin.git` and two clones, `a` and `b`.
Work through the questions below by actually running things.

1. Commit in `a` and push. In `b` pull, commit and push. Now in `a` amend the old commit and try `git push --force-with-lease`. What happens and why does the lease refuse? How is this safer than `--force`?
2. What does `--force-with-lease=<ref>:<expect>` let you pin explicitly, and when is the plain form unreliable (hint: background `git fetch`)?
3. Create a lightweight tag and an annotated tag. Which `git cat-file -t` output does each give? Which one does `git describe` use by default, and what flag changes that?
4. How do you push a single tag, push all tags, and delete a remote tag?

## WHAT I RAN

```bash
mkdir -p /tmp/day46-lab && cd /tmp/day46-lab
git init -q --bare origin.git
git clone -q origin.git a && git clone -q origin.git b
cd a && echo 1 > f && git add f && git commit -qm "a1" && git push -q origin HEAD
cd ../b && git pull -q && echo 2 >> f && git commit -qam "b2" && git push -q origin HEAD
cd ../a && git commit -q --amend -m "a1 amended"
git push --force-with-lease origin HEAD      # rejected (stale info)
git push --force origin HEAD                 # would silently destroy b2

git tag light
git tag -a annotated -m "release"
git cat-file -t light        # commit
git cat-file -t annotated    # tag
git describe                 # annotated tags only
git describe --tags          # also lightweight
git push origin annotated    # single tag
git push origin --tags       # all tags
git push origin --delete annotated   # delete remote tag (or :refs/tags/annotated)
```

## MY ANSWERS

1. The push is rejected ("stale info"). `a` last saw origin at a1, but origin now holds b2 on top of it. `--force-with-lease` only overwrites the remote ref if it still equals what my remote-tracking branch says, so it detects that someone else pushed in between and refuses. Plain `--force` would overwrite b2 without any check, so the lease is much safer.
2. `--force-with-lease=<ref>:<expect>` pins the exact commit I expect the remote ref to be at (e.g. `--force-with-lease=main:abc123`). The plain form compares against the remote-tracking branch, which a background `git fetch` (IDE, cron) can update without me looking at the new commits; then the lease passes and I overwrite work I never reviewed. Pinning the expected sha avoids that.
3. Lightweight tag: `git cat-file -t` prints `commit` (just a ref pointing at the commit). Annotated tag: prints `tag` (a real object with tagger, date, message, optional signature). `git describe` uses annotated tags by default; `--tags` includes lightweight ones too.
4. Single tag: `git push origin <tagname>`. All tags: `git push origin --tags`. Delete a remote tag: `git push origin --delete <tagname>` (or `git push origin :refs/tags/<tagname>`); delete locally with `git tag -d <tagname>`.
