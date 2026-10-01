# Day 11, Task 6 -- Git: finding when and why a line changed

## THE TASK

Earlier days covered bisect, reflog, tags and worktrees. This one is
about history archaeology: `git log -S` / `-G` (the pickaxe), `git log
-L`, and `git blame` with its noise filters.

1. In a SCRATCH repo (`/tmp/archaeology`, `git init -b main`), build a
   small history of at least 5 commits on `app.py`: add a function
   `price()` containing the constant `TAX = 0.13`, later change it to
   `0.15`, rename the function to `compute_price()`, and make one
   whitespace-only reformat commit.
2. Use `git log -S"0.13"` to find the commit that added or removed that
   string. How does `-S` differ from `-G"0\.1[35]"` (regex, matches any
   commit whose diff has a changed line matching)?
3. Use `git log -L :compute_price:app.py` to see the history of just
   that function. What does it show that plain `git log -p` does not?
4. Run `git blame app.py`, then `git blame -w` and `git blame
   --ignore-rev <whitespace-commit-sha>`. What changes in the output?
5. Put the whitespace commit's sha in a `.git-blame-ignore-revs` file
   and set `git config blame.ignoreRevsFile .git-blame-ignore-revs`.
   When is this worth doing in a real project?

## WHAT I RAN

```
TODO: paste the commands you actually ran, in order
```

## WHAT EACH COMMAND SHOWED (write AFTER)

- `-S"0.13"` vs `-G`: TODO
- `-L :compute_price:app.py`: TODO
- `blame` vs `blame -w` vs `--ignore-rev`: TODO

## PICKAXE vs BLAME vs BISECT (write in your own words)

TODO: for each of "who last touched this line", "when did this string
first appear", and "when did this behaviour break", say which tool you
would reach for and why.
