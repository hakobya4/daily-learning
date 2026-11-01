#!/usr/bin/env bash
#
# Day 41, Task 5 -- Unix/shell: join backslash-continued lines.
#
# THE PROBLEM
# ------------
# Read text on stdin. A line ending in a backslash continues on the next line:
# remove the backslash, the newline, and the next line's LEADING whitespace,
# and put exactly one space at the join (chains of continuations are allowed).
# Lines not ending in a backslash pass through unchanged.
#
# HINT: awk with a buffer variable (sub(/\\$/, "") then append next line with
# leading blanks stripped) or sed with a N/ba loop.
#
# Check with:
#   printf 'cc -o app\\\n    main.c\\\n    util.c\necho done\n' | ./join_continuation_lines.sh
# Expected:
#   cc -o app main.c util.c
#   echo done

# TODO: replace this line
exit 1
