#!/usr/bin/env bash
#
# Day 41, Task 4 -- Unix/shell: maximum of each column.
#
# THE PROBLEM
# ------------
# Read whitespace-separated numeric rows on stdin (rows may have different
# lengths). Print ONE line: the maximum of each column, separated by single
# spaces. Column k's max only considers rows that have a k-th field. Empty
# input prints nothing. Numbers may be negative or decimal.
#
# HINT: awk, keep an array max[i] and a variable for the widest NF; use
# (i in max) to detect the first value seen. END block prints.
#
# Check with:
#   printf '1 5 3\n4 2\n-1 9 8 7\n' | ./max_per_column.sh
# Expected:
#   4 9 8 7

awk '{
  for (i = 1; i <= NF; i++)
    if (!(i in max) || $i + 0 > max[i] + 0) max[i] = $i
  if (NF > w) w = NF
}
END {
  if (NR == 0) exit
  line = ""
  for (i = 1; i <= w; i++) line = line (i > 1 ? " " : "") max[i]
  print line
}'
