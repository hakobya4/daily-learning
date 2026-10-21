# Day 30, Task 7 -- Git: plumbing (`cat-file`, `ls-files -s`, `rev-parse`), `git grep`, `diff-filter`

## THE TASK

In a SCRATCH repo (`/tmp/day30-lab`, `git init -b main`, a few commits including one that deletes a file and one that renames a file):

1. How do you print the type and content of an object by hash (`git cat-file -t` / `-p`)? What do the objects behind a commit, a tree and a file look like?
2. What does `git ls-files -s` show in each column, and what does the stage number mean during a merge conflict?
3. What do `git rev-parse HEAD~2`, `HEAD^{tree}` and `--show-toplevel` return, and when would you use each in a script?
4. How do you search file contents at a past revision with `git grep` (`git grep -n pattern <rev>`)? How does it differ from plain `grep -r`?
5. How do you list only the commits that DELETED a file (`git log --diff-filter=D --name-only`)? What do the other filter letters (A, M, R) mean?

## WHAT I RAN

```bash
git init -b main /tmp/day30-lab && cd /tmp/day30-lab
echo one > a.txt && echo keep > b.txt && git add . && git commit -m "add a and b"
echo two >> a.txt && git commit -am "edit a"
git mv a.txt renamed.txt && git commit -m "rename a to renamed"
git rm b.txt && git commit -m "delete b"
git cat-file -t HEAD && git cat-file -p HEAD
git cat-file -p 'HEAD^{tree}'
git ls-files -s
git rev-parse HEAD~2 'HEAD^{tree}' --show-toplevel
git grep -n one HEAD~3
git log --diff-filter=D --name-only --oneline
```

## MY ANSWERS

1. `git cat-file -t <hash>` prints the object type (commit, tree, blob, tag) and `-p` pretty-prints its content. A commit object holds the hash of one tree, zero or more parent hashes, author and committer lines and the message. A tree lists entries of `mode type hash name` (a directory snapshot pointing to blobs and sub-trees). A blob is just the raw bytes of one file version, with no name or metadata.
2. Columns are `mode  blob-hash  stage-number  path`. Stage 0 is a normal, resolved entry. During a merge conflict the index holds up to three entries for the path: stage 1 = common ancestor, stage 2 = ours (HEAD), stage 3 = theirs. Resolving and `git add`-ing the file collapses them back to stage 0.
3. `HEAD~2` is the full hash of the grandparent commit (follow first parents twice), handy for scripting ranges or checkouts. `HEAD^{tree}` is the hash of the tree of HEAD, useful for comparing content independent of history. `--show-toplevel` prints the absolute path of the working tree root, so a script can `cd "$(git rev-parse --show-toplevel)"` no matter where it was started.
4. `git grep -n pattern <rev>` searches the files as they were in that revision (output prefixed `rev:path:line:`) without checking it out. Unlike `grep -r`, it only looks at tracked files (or the objects of the rev), ignores `.git` and untracked/ignored junk, is faster because it reads from the index/object store, and can search any commit, not just the working tree.
5. `git log --diff-filter=D --name-only` shows only commits that deleted at least one file, listing the deleted names. Filter letters: A = added, M = modified, R = renamed, D = deleted (also C copied, T type changed, U unmerged); lowercase excludes that kind. Combine with `-- path` to find when a specific file was removed.
