#!/usr/bin/env bash
#
# Day 31, Task 6 -- Unix/shell: running maximum.
#
# THE PROBLEM
# ------------
# stdin has one number per line (integers, possibly negative). For every
# line print the largest value seen so far, including the current line.
#   3 1 4 1 5 9 2 6   ->   3 3 4 4 5 9 9 9   (one per line)
#   -5 -2 -9          ->   -5 -2 -2
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk with a first-line special case (NR == 1 || $1 > max) so negative
# numbers work -- do NOT start max at 0.
#
# Check with:
#   printf '3\n1\n4\n1\n5\n9\n2\n6\n' | ./running_max.sh
# Expected:
#   3
#   3
#   4
#   4
#   5
#   9
#   9
#   9

awk 'NF { if (n++ == 0 || $1 + 0 > max) max = $1 + 0; print max }'
