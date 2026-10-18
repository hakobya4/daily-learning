#!/usr/bin/env bash
#
# Day 27, Task 5 -- Unix/shell: swap the first and last word of each line.
#
# THE PROBLEM
# ------------
# For every line on stdin (words separated by whitespace), print the line
# with its first and last words swapped, words joined by single spaces.
# Lines with fewer than 2 words are printed unchanged. Blank lines stay
# blank.
#
#   input:  the quick brown fox
#   output: fox quick brown the
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: NF is the field count; swap $1 and $NF via a temp variable, then
# print $0 (assigning to a field rebuilds $0 with single spaces).
#
# Check with:
#   printf 'the quick brown fox\nhello\n\na b\n' | ./swap_first_last_word.sh
# Expected:
#   fox quick brown the
#   hello
#
#   b a

awk '{ if (NF >= 2) { t = $1; $1 = $NF; $NF = t } print }'
