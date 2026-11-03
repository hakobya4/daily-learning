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
# TODO: paste your commands and their output here
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
