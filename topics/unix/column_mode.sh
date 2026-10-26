#!/usr/bin/env bash
#
# Day 36, Task 5 -- Unix/shell: most frequent value in a CSV column.
#
# THE PROBLEM
# ------------
# stdin is a CSV (comma-separated, NO quoting) with a header row. Print the
# most frequent value of column 2 (ignoring the header) followed by a
# space and its count. On a tie, print the alphabetically smallest value.
# No data rows -> print nothing.
#
# Input:
#   id,color
#   1,red
#   2,blue
#   3,red
#   4,blue
#   5,green
# Output:
#   blue 2
#
# HINT: tail -n +2 | cut -d, -f2 | sort | uniq -c | sort -k1,1nr -k2,2 | head -1
# (then reformat "count value" -> "value count"; or do it all in awk).
#
# Check with:
#   printf 'id,color\n1,red\n2,blue\n3,red\n4,blue\n5,green\n' | ./column_mode.sh
# Expected:
#   blue 2

# TODO: replace this line
exit 1
