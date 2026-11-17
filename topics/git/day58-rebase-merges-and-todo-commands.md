# Day 58, Task 8 -- Git: `rebase --rebase-merges` and the todo-list commands (`label`, `reset`, `merge`, `exec`, `break`)

## THE TASK

In a SCRATCH repo (`/tmp/day58-lab`, `git init -b main`) build this history: `main` with 2 commits, then a branch `feature` off `main` that contains its OWN merge -- a sub-branch `feature-ui` (2 commits) merged into `feature` with `--no-ff` -- plus one more commit on `feature` after that merge. Meanwhile add 1-2 new commits on `main`. Then answer the questions by actually running the commands -- never in a real project's history.

1. Rebase `feature` onto the new `main` with a PLAIN `git rebase main`. What happens to the inner merge commit? Draw the graph before and after (`git log --graph --oneline --all`). Undo it with the reflog (`git reset --hard feature@{1}` or `ORIG_HEAD`) and explain which of the two you used and why it is the right one.
2. Now rebase with `git rebase -i --rebase-merges main` (`-r`). Paste the generated todo list and explain every `label`, `reset` and `merge -C <hash>` line. What do `onto` and the auto-generated label names refer to? What does `merge -c` (lower case) do differently from `merge -C`?
3. In the same kind of todo list, insert an `exec make test || false`-style line (use `exec test -f notes.txt` or any command that can fail) after one `pick`, and a `break` after another. What happens when the `exec` command fails and how do you continue? What does `break` do, and how is it different from `edit`?
4. Run `git rebase -r --exec "git log -1 --oneline" main`: where does git insert the `exec` lines in a todo list that contains merges? Then explain `--rebase-merges=rebase-cousins` vs. the default `no-rebase-cousins` (make one commit on `feature-ui` whose parent is NOT a descendant of `feature`'s base to see the difference, or explain from the docs if you cannot reproduce it), and what `git pull --rebase=merges` / `pull.rebase = merges` do.

## WHAT I RAN

```bash
# TODO: build the lab history (main, feature, feature-ui with a --no-ff merge, new main commits)


# Q1: plain rebase, then undo


# Q2: rebase --rebase-merges (paste the todo list below)


# Q3: exec + break in the todo list


# Q4: --exec with -r, rebase-cousins
```

## ANSWERS

1. **Plain rebase and the inner merge:**
   TODO

2. **The `-r` todo list (`label` / `reset` / `merge -C`):**
   ```
   TODO: paste the generated todo list
   ```
   TODO: explain each line, `onto`, and `merge -c` vs `merge -C`

3. **`exec` failing and `break` vs `edit`:**
   TODO

4. **`--exec` placement, `rebase-cousins`, `pull --rebase=merges`:**
   TODO

## ONE-LINE TAKEAWAY

TODO
