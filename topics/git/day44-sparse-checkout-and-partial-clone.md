# Day 44, Task 7 -- Git: sparse-checkout and partial clone

## THE TASK

In a SCRATCH area (`/tmp/day44-lab`) create a "server" repo with 3 top-level
directories (`app/`, `docs/`, `assets/`), each with a few files and at least
2 commits. Then clone it with `--filter=blob:none --no-checkout` (use
`file://` URL and run `git config uploadpack.allowFilter true` on the server
first) and work through the questions.

1. What does `--filter=blob:none` change about what is downloaded, and when does git fetch the missing blobs later?
2. Run `git sparse-checkout init --cone` then `git sparse-checkout set app`. What ends up in the working tree? What is the difference between cone mode and non-cone mode patterns?
3. How do you see which patterns are active, and how do you go back to a full checkout (`disable`)?
4. How do you verify which objects are missing locally (`git rev-list --objects --missing=print --all`)? What does the `?` prefix mean?
5. Compare `--depth 1` (shallow) with `--filter=blob:none` (partial): what history/data does each one lack?

## WHAT I RAN

```bash
cd /tmp/day44-lab && git init srv && cd srv
git config uploadpack.allowFilter true
mkdir app docs assets; echo 1 > app/a.txt; echo 1 > docs/d.md; echo 1 > assets/x.png
git add . && git commit -m c1
echo 2 >> app/a.txt; echo 2 >> docs/d.md; git commit -am c2
cd .. && git clone --filter=blob:none --no-checkout file:///tmp/day44-lab/srv cl
cd cl
git rev-list --objects --missing=print --all   # blobs listed with a leading "?"
git sparse-checkout set --cone app
git checkout master                            # fetches only app/ blobs now
ls                                             # -> app
git sparse-checkout list                       # -> app
git sparse-checkout disable                    # back to full checkout
```

## MY ANSWERS

1. `--filter=blob:none` downloads all commits and trees but no file contents (blobs). Blobs are fetched lazily from the promisor remote when something needs them: a checkout, `git diff`, `git show`, `git blame`, etc. Batches are requested on demand.
2. Only the files at the repo root plus the `app/` directory appear in the working tree; `docs/` and `assets/` are absent. Cone mode takes plain directory names and includes everything under them (plus files directly in their parents), and is fast. Non-cone mode takes full gitignore-style patterns (globs, negations) and is slower and more error-prone.
3. `git sparse-checkout list` shows the active patterns/directories (stored in `.git/info/sparse-checkout`). `git sparse-checkout disable` restores the full working tree (missing blobs are then fetched).
4. `git rev-list --objects --missing=print --all` lists all reachable objects and prints the ones absent locally with a `?` prefix, i.e. the not-yet-downloaded blobs of a partial clone.
5. `--depth 1` (shallow) truncates history: you get only the latest commit (and its full tree and blobs), but no older commits. `--filter=blob:none` (partial) keeps the full commit history and trees but omits blob contents until needed. Shallow cannot do log/blame over history; partial can, but needs the remote online to fetch blobs.
