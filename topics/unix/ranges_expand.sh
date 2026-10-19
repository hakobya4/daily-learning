#!/usr/bin/env bash
#
# Day 29, Task 5 -- Unix/shell: expand number ranges.
#
# THE PROBLEM
# ------------
# Each stdin line is a comma-separated list of numbers and ranges, e.g.
# "1-3,7,10-12". Print each line expanded into a space-separated list of
# integers, in the order written:
#   1-3,7,10-12   ->   1 2 3 7 10 11 12
#   5             ->   5
#   4-4,2         ->   4 2
# Blank lines print a blank line.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: split($0, parts, ","), then for each part split(part, ab, "-"):
# if ab[2] is empty it is a single number, otherwise loop ab[1]..ab[2].
# Build the output with a separator variable so there is no trailing space.
#
# Check with:
#   printf '1-3,7,10-12\n5\n4-4,2\n' | ./ranges_expand.sh
# Expected:
#   1 2 3 7 10 11 12
#   5
#   4 2

# TODO: replace this line
echo "not implemented" >&2; exit 1
