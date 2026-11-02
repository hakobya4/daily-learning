#!/usr/bin/env bash
#
# Day 43, Task 4 -- Unix/shell: count runs of consecutive identical lines.
#
# THE PROBLEM
# ------------
# Usage: ./consecutive_dup_count.sh < file
# Collapse each RUN of identical adjacent lines into one output line of the
# form "<count> <line>". Unlike `sort | uniq -c`, the input is NOT sorted and
# the same line may appear again later as a new run.
#
# HINT: awk with a prev variable and a counter; flush in the END block.
#       (`uniq -c` pads counts with spaces -- the expected output below has
#       a single space, so awk/printf is easier.)
#
# Check with:
#   printf 'a\na\nb\na\na\na\n' | ./consecutive_dup_count.sh
# Expected:
#   2 a
#   1 b
#   3 a
#   printf '' | ./consecutive_dup_count.sh   -> prints nothing

# TODO: replace this line
exit 1
