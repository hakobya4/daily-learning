#!/usr/bin/env bash
#
# Day 38, Task 5 -- Unix/shell: dedupe keeping the LAST occurrence.
#
# THE PROBLEM
# ------------
# Read stdin. Print each distinct line exactly once, but at the position of
# its LAST occurrence (so output order = order of last appearance).
#
# Input (stdin), one per line:  a b a c b
# Output:
#   a
#   c
#   b
#
# HINT: read the file twice (tac | awk '!seen[$0]++' | tac) -- reverse, keep
# first sight, reverse again.
#
# Check with:
#   printf 'a\nb\na\nc\nb\n' | ./last_occurrence_dedupe.sh
# Expected:
#   a
#   c
#   b

# TODO: replace this line
exit 1
