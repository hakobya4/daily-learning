#!/usr/bin/env bash
#
# Day 26, Task 5 -- Unix/shell: number the non-blank lines.
#
# THE PROBLEM
# ------------
# Read stdin. Prefix every NON-blank line with its running number, a colon
# and a space ("1: text"). Blank lines (empty or only whitespace) are
# printed unchanged, empty, and do NOT increase the counter.
#
#   input:  a / (blank) / b / c
#   output: 1: a / (blank) / 2: b / 3: c
#
# HOW TO WORK THROUGH THIS
# -------------------------
# One awk program: test `$0 ~ /^[ \t]*$/` for blank lines.
#
# Check with:
#   printf 'a\n\nb\nc\n' | ./number_nonblank.sh

# TODO: replace this line
exit 1
