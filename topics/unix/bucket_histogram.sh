#!/usr/bin/env bash
#
# Day 26, Task 6 -- Unix/shell: bucket numbers into ranges of 10.
#
# THE PROBLEM
# ------------
# stdin has one non-negative integer per line (skip blank lines). Print one
# line "LO-HI COUNT" per NON-EMPTY bucket of width 10, ordered by LO
# ascending. Bucket 0 is 0-9, bucket 1 is 10-19, and so on.
#
#   input:  3 7 12 15 18 41
#   output: 0-9 2
#           10-19 3
#           40-49 1
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: b = int($1/10); count[b]++; track the max b and loop 0..max in END
# (skipping zero counts) so the order is numeric, not string.
#
# Check with:
#   printf '3\n7\n12\n15\n18\n41\n' | ./bucket_histogram.sh

# TODO: replace this line
exit 1
