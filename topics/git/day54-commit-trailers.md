# Day 54, Task 8 -- Git: commit trailers (`--trailer`, `interpret-trailers`, `%(trailers)`)

## THE TASK

In a SCRATCH repo (`/tmp/day54-lab`, `git init`, a few commits) explore commit trailers -- the `Key: value` lines at the end of a commit message (`Signed-off-by:`, `Co-authored-by:`, `Reviewed-by:`, `Fixes:` ...). Work through the questions by actually running things -- never in a real project's history.

1. Make one commit with `git commit -s` and another with `git commit --trailer "Reviewed-by: Ana <ana@example.com>" --trailer "Fixes: #12"`. Show the full messages (`git log -2 --format=%B`). Where exactly do the trailers end up, and why does git need a blank line before the trailer block? What happens if the message body's last paragraph already looks like `Key: value`?
2. Pipe a message file through `git interpret-trailers` (no commit involved): add a trailer with `--trailer`, then try `--if-exists addIfDifferent`, `--if-exists replace` and `--if-missing doNothing`. Which option stops a duplicate `Signed-off-by:` from the same person being added twice?
3. Extract trailers from history: compare `git log --format="%(trailers)"`, `%(trailers:key=Reviewed-by)`, `%(trailers:key=Fixes,valueonly)` and `%(trailers:only,unfold)`. Write ONE command that lists every commit hash with its `Fixes:` value, skipping commits that have none.
4. Configure a trailer alias in the scratch repo's LOCAL config (`git config trailer.rb.key "Reviewed-by"` etc.) so `--trailer "rb: Ana"` expands to `Reviewed-by: Ana`. Why do hosting sites (e.g. GitHub's `Co-authored-by:`) care that the trailer format is exact, and what does `git shortlog --group=trailer:co-authored-by` show?

## WHAT I RAN

```bash
# TODO: fill in the exact commands you ran
```

## MY ANSWERS

1. TODO
2. TODO
3. TODO
4. TODO
