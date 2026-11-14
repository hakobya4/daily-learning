# Day 54, Task 8 -- Git: commit trailers (`--trailer`, `interpret-trailers`, `%(trailers)`)

## THE TASK

In a SCRATCH repo (`/tmp/day54-lab`, `git init`, a few commits) explore commit trailers -- the `Key: value` lines at the end of a commit message (`Signed-off-by:`, `Co-authored-by:`, `Reviewed-by:`, `Fixes:` ...). Work through the questions by actually running things -- never in a real project's history.

1. Make one commit with `git commit -s` and another with `git commit --trailer "Reviewed-by: Ana <ana@example.com>" --trailer "Fixes: #12"`. Show the full messages (`git log -2 --format=%B`). Where exactly do the trailers end up, and why does git need a blank line before the trailer block? What happens if the message body's last paragraph already looks like `Key: value`?
2. Pipe a message file through `git interpret-trailers` (no commit involved): add a trailer with `--trailer`, then try `--if-exists addIfDifferent`, `--if-exists replace` and `--if-missing doNothing`. Which option stops a duplicate `Signed-off-by:` from the same person being added twice?
3. Extract trailers from history: compare `git log --format="%(trailers)"`, `%(trailers:key=Reviewed-by)`, `%(trailers:key=Fixes,valueonly)` and `%(trailers:only,unfold)`. Write ONE command that lists every commit hash with its `Fixes:` value, skipping commits that have none.
4. Configure a trailer alias in the scratch repo's LOCAL config (`git config trailer.rb.key "Reviewed-by"` etc.) so `--trailer "rb: Ana"` expands to `Reviewed-by: Ana`. Why do hosting sites (e.g. GitHub's `Co-authored-by:`) care that the trailer format is exact, and what does `git shortlog --group=trailer:co-authored-by` show?

## WHAT I RAN

```bash
mkdir /tmp/day54-lab && cd /tmp/day54-lab
git init -b main
git config user.name Narek; git config user.email narek@example.com
echo a>a; git add a; git commit -m "init"

# Q1: -s and --trailer (needs git >= 2.32 for commit --trailer)
echo b>b; git add b; git commit -s -m "add b"
echo c>c; git add c; git commit -m "add c" \
    --trailer "Reviewed-by: Ana <ana@example.com>" --trailer "Fixes: #12"
git log -2 --format=%B
# last paragraph that already LOOKS like a trailer:
echo d>d; git add d; git commit -m "add d

Note: this paragraph looks like a trailer" --trailer "Fixes: #13"
git log -1 --format=%B
git log -1 --format='%(trailers:only,unfold)'   # shows BOTH "Note:" and "Fixes:" as trailers

# Q2: interpret-trailers on a plain file, no commit involved
printf 'subject\n\nbody\n\nSigned-off-by: Narek <narek@example.com>\n' > msg.txt
git interpret-trailers --trailer "Acked-by: Bob <b@x>" msg.txt
git interpret-trailers --if-exists addIfDifferent  --trailer "Signed-off-by: Narek <narek@example.com>" msg.txt
git interpret-trailers --if-exists add             --trailer "Signed-off-by: Narek <narek@example.com>" msg.txt
git interpret-trailers --if-exists replace         --trailer "Signed-off-by: Bob <b@x>" msg.txt
git interpret-trailers --if-missing doNothing      --trailer "Acked-by: Bob <b@x>" msg.txt

# Q3: reading trailers back out of history
git log --format="%h%n%(trailers)"
git log --format="%h %(trailers:key=Reviewed-by)"
git log --format="%h %(trailers:key=Fixes,valueonly)"
git log --format="%h%n%(trailers:only,unfold)"
git log --format='%h %(trailers:key=Fixes,valueonly,separator=%x2C)' | awk 'NF > 1'

# Q4: trailer alias in LOCAL config + co-author grouping
git config trailer.rb.key "Reviewed-by"
echo e>e; git add e; git commit -m "add e" --trailer "rb: Ana <ana@example.com>"
git log -1 --format=%B                         # -> Reviewed-by: Ana <ana@example.com>
git commit --allow-empty -m "pair" --trailer "Co-authored-by: Ana <ana@example.com>"
git shortlog -s --group=trailer:co-authored-by HEAD
```

## MY ANSWERS

1. Both `-s` and `--trailer` put the trailers in ONE block at the very end of the message, separated from the body by a blank line: `add b` / blank / `Signed-off-by: Narek <...>`, and `add c` / blank / `Reviewed-by: Ana <...>` / `Fixes: #12` in the order I gave them. Git needs the blank line because a "trailer block" is defined as the LAST paragraph of the message, and every line in it (well, at least 25% of lines, with at least one git-generated or configured trailer) must look like `Key: value`. Without the blank line the trailers would just be part of the subject/body paragraph and parsers would not find them. The flip side: if the last paragraph of the body already looks like `Key: value` (my `Note: this paragraph looks like a trailer`), git treats that paragraph AS the trailer block and appends to it -- the `Fixes: #13` was added directly under `Note: ...` with no blank line, and `%(trailers:only)` then reported `Note:` as a trailer too. To avoid that, end the body with a normal sentence, or don't use a colon-style line as the last paragraph.
2. `git interpret-trailers` reads a message (file or stdin), parses the trailer block, and prints the message with trailers added/changed -- it never touches a commit, which makes it handy in `commit-msg`/`prepare-commit-msg` hooks. `--if-exists addIfDifferent` adds the trailer only if NO existing trailer has the same key AND value, so it is the option that stops a second identical `Signed-off-by: Narek <...>` (it printed the message unchanged). `--if-exists add` always appends, giving a duplicate. `--if-exists replace` removes the existing `Signed-off-by:` and puts the new one (mine became `Signed-off-by: Bob <b@x>`). `--if-missing doNothing` means "only act if a trailer with this key already exists" -- my `Acked-by:` was not added because there was none. (Side note: the built-in default is `addIfDifferentNeighbor`, which also skipped the duplicate here only because the identical sign-off happened to be the LAST trailer; with a different trailer in between it would have added it again. `-s` itself also has this "don't repeat if already last" behaviour.)
3. `%(trailers)` prints the whole trailer block as-is; `%(trailers:key=Reviewed-by)` prints only matching trailers but still as `Reviewed-by: Ana <...>` (key matching is case-insensitive); adding `valueonly` drops the `Key: ` part, so `%(trailers:key=Fixes,valueonly)` gives just `#12`; `only` keeps only real `Key: value` lines (drops non-trailer lines that sit in the block) and `unfold` joins multi-line (continuation-line) trailer values onto one line. My one-liner, printing hash + Fixes value and skipping commits without one (multiple Fixes joined by commas):

   ```bash
   git log --format='%h %(trailers:key=Fixes,valueonly,separator=%x2C)' | awk 'NF > 1'
   ```

   Output here: `7e88bdb #13` and `568286e #12`. (Without awk, every commit would print a line with an empty value; there is no format-level "skip if empty".)
4. `git config trailer.rb.key "Reviewed-by"` (local, inside the lab repo only) makes `rb` an alias: `--trailer "rb: Ana <ana@example.com>"` produced `Reviewed-by: Ana <ana@example.com>`. You can also set `trailer.<alias>.ifexists`, `.ifmissing`, `.where` or `.cmd` (a command that generates the value) per alias. Hosting sites care about the exact format because they parse it mechanically: GitHub only credits a co-author when the line is exactly `Co-authored-by: Name <email>` in the trailer block, after a blank line, with an email linked to an account -- a typo in the key, a missing blank line, or the trailer in the middle of the body and no avatar/contribution appears. Same idea for `Signed-off-by:` checks (DCO bots) and `Fixes:` / `Closes:` automation. `git shortlog --group=trailer:co-authored-by` groups commits by the VALUE of that trailer instead of by author, so it counts co-authorship: here it printed `1  Ana` (my "pair" commit). You can combine groups (`--group=author --group=trailer:co-authored-by`) to count each commit for both the author and the co-authors.
