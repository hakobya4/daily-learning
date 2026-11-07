#!/usr/bin/env bash
#
# Day 47, Task 4 -- Unix/shell: append a total column to a CSV.
#
# THE PROBLEM
# ------------
# Usage: ./csv_row_totals.sh FILE
# FILE is a comma-separated file of integers with a header row (no quoting,
# no spaces). Print the header with ",total" appended, then every data row with
# the sum of its fields appended. Skip blank lines. Exit 1 on bad usage or an
# unreadable FILE.
#
# HINT: awk -F, with OFS=","; NR==1 handles the header; loop i=1..NF to sum.
#
# Check with:
#   printf 'a,b,c\n1,2,3\n4,5,-6\n' > /tmp/d47a; ./csv_row_totals.sh /tmp/d47a
# Expected:
#   a,b,c,total
#   1,2,3,6
#   4,5,-6,3

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi
awk -F, 'BEGIN { OFS = "," }
  NF == 0 { next }
  NR == 1 { print $0, "total"; next }
  { s = 0; for (i = 1; i <= NF; i++) s += $i; print $0, s }' "$1"
