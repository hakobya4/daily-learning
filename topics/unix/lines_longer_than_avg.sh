#!/usr/bin/env bash
#
# Day 28, Task 5 -- Unix/shell: print lines longer than the average line.
#
# THE PROBLEM
# ------------
# Read all of stdin. Print (in original order) every line whose length in
# characters is STRICTLY greater than the average line length. Empty input
# prints nothing.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Two passes are needed, but stdin can only be read once: store every line
# in an array in the main block, accumulate the total length, then compare
# in an END block (average = total / NR).
#
# Check with:
#   printf 'aa\nbbbbbb\ncccc\nd\n' | ./lines_longer_than_avg.sh
# (lengths 2,6,4,1 -> average 3.25) Expected:
#   bbbbbb
#   cccc

# TODO: replace this line
exit 1
