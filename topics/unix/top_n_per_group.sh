#!/usr/bin/env bash
#
# Day 15, Task 6 -- Unix/shell: top 2 values per group.
#
# THE PROBLEM
# ------------
# stdin has lines "group value" (value is an integer). For each group
# print its two largest values as "group v1 v2" (largest first). A group
# with one line prints just "group v1". Groups come out sorted
# alphabetically. Duplicated values count separately.
#
#   input:  a 5 / b 1 / a 9 / a 7 / b 4 / c 2
#   output: a 9 7 / b 4 1 / c 2
#
# HOW TO WORK THROUGH THIS
# -------------------------
# sort -k1,1 -k2,2nr then awk keeping a per-group counter, or collect in
# awk arrays and sort the group names at the end.
#
# Check with:
#   printf 'a 5\nb 1\na 9\na 7\nb 4\nc 2\n' | ./top_n_per_group.sh
#   -> a 9 7 / b 4 1 / c 2

# TODO: replace this line
exit 1
