# Day 38, Task 7 -- Git: submodules basics

## THE TASK

In a SCRATCH area (`/tmp/day38-lab`) create two repos: `lib` (one commit) and `app`. Practice submodules.

1. How do you add `lib` as a submodule of `app`, and which two things does `git add`/commit record (hint: `.gitmodules` and a special tree entry)? What mode is that entry?
2. After someone clones `app`, the submodule directory is empty. Which commands (or clone flag) fetch it?
3. `lib` gets a new commit. How do you update `app` to point to it, and how does `git status`/`git diff` in `app` show the change?
4. What does `git submodule update --init --recursive` do versus `git submodule update --remote`?
5. How do you cleanly remove a submodule (three places to clean)?

## WHAT I RAN

```bash
mkdir -p /tmp/day38-lab && cd /tmp/day38-lab
git init -b main lib && cd lib && echo v1 > lib.txt && git add . && git commit -m "lib v1" && cd ..
git init -b main app && cd app && git commit --allow-empty -m "app init"
git -c protocol.file.allow=always submodule add ../lib libdir
git commit -m "add lib submodule"
git ls-files -s libdir                     # mode 160000
cat .gitmodules
cd .. && git clone app app-clone && ls app-clone/libdir        # empty
cd app-clone && git submodule update --init --recursive        # (or: git clone --recurse-submodules)
cd ../lib && echo v2 >> lib.txt && git commit -am "lib v2" && cd ../app
git submodule update --remote libdir       # moves submodule to lib's latest
git status; git diff --submodule          # shows "new commits" / pointer change
git add libdir && git commit -m "bump lib"
# remove
git submodule deinit -f libdir
git rm -f libdir
rm -rf .git/modules/libdir
git commit -m "remove lib submodule"
```

## MY ANSWERS

1. `git submodule add <url> <path>` clones the repo into `<path>` and stages two things: a new `.gitmodules` file (path and url) and a special tree entry at `<path>` that records the exact commit of the submodule (a "gitlink"). The entry's mode is `160000`. Commit both.
2. A normal clone leaves the submodule directory empty. Run `git submodule update --init --recursive` afterwards, or clone with `git clone --recurse-submodules <url>`.
3. Inside the submodule `git pull` / `git checkout` the new commit (or from the parent run `git submodule update --remote <path>`), then in the parent `git add <path>` and commit. Before committing, `git status` shows `modified: libdir (new commits)` and `git diff --submodule` lists the commits; the parent's diff is just old sha -> new sha.
4. `git submodule update --init --recursive` initializes missing submodules (including nested ones) and checks out the commit RECORDED in the parent, which gives a detached HEAD. `git submodule update --remote` ignores the recorded commit and fetches the tip of the submodule's tracked branch (default `main`/`master`, or `branch` in `.gitmodules`), so the parent then shows a changed pointer.
5. Three places to clean: (a) the registration, `git submodule deinit -f <path>` (removes it from `.git/config` and empties the working dir); (b) the parent's index and `.gitmodules`, `git rm -f <path>` and commit; (c) the cached repo `rm -rf .git/modules/<path>`.
