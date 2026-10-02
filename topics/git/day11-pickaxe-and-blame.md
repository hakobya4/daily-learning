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
rm -rf /tmp/archaeology && mkdir /tmp/archaeology && cd /tmp/archaeology
git init -b main
printf 'def price(x):\n    TAX = 0.13\n    return x * (1 + TAX)\n' > app.py
git add app.py && git commit -m "add price()"
printf 'def price(x):\n    TAX = 0.13\n    return x * (1 + TAX)\n\n\ndef other():\n    return 1\n' > app.py
git commit -am "add other()"
sed -i 's/0.13/0.15/' app.py && git commit -am "raise tax to 0.15"
sed -i 's/def price/def compute_price/' app.py && git commit -am "rename price -> compute_price"
sed -i 's/x \* (1 + TAX)/x*(1+TAX)/' app.py && git commit -am "whitespace reformat"
git log -S"0.13" --oneline
git log -G"0\.1[35]" --oneline
git log -L :compute_price:app.py
git blame app.py
git blame -w app.py
git blame --ignore-rev $(git rev-parse HEAD) app.py
git rev-parse HEAD > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

## WHAT EACH COMMAND SHOWED (write AFTER)

- `-S"0.13"` vs `-G`: `-S` lists only commits where the NUMBER OF OCCURRENCES of the string changed (the commit that added 0.13 and the one that replaced it with 0.15). `-G` is a regex over the changed lines of the diff, so it also matches commits where a matching line was merely modified (e.g. 0.13 -> 0.15 and the reformat if it touched a matching line). `-S` finds "when did it appear/disappear"; `-G` finds "when was any line like this touched".
- `-L :compute_price:app.py`: shows each commit that changed that function, with only the diff hunks of that function (following it through the rename), instead of whole-file diffs for every commit like plain `git log -p`.
- `blame` vs `blame -w` vs `--ignore-rev`: plain blame attributes the reformatted line to the whitespace commit. `-w` ignores whitespace-only differences when deciding who changed a line, so blame points back to the earlier real change. `--ignore-rev <sha>` skips that specific commit entirely and passes blame to the previous commit that touched the line; it also works for bulk changes `-w` cannot hide (renames, moved code, auto-formatter runs). A `.git-blame-ignore-revs` file is worth it when a project does mass reformatting or formatter adoption; GitHub honours that file name too.

## PICKAXE vs BLAME vs BISECT (write in your own words)

- "Who last touched this line": `git blame` (with `-w` / ignore-revs to skip noise), since it maps each current line to the commit that last changed it.
- "When did this string first appear": `git log -S"string"` (or `-G` for a regex), since it searches history for changes in occurrence count rather than current lines.
- "When did this behaviour break": `git bisect` with a test, since the break may not involve any particular string; it binary-searches commits by good/bad outcome.
