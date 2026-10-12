#!/usr/bin/env bash
#
# Day 21, Task 6 -- Unix/shell: sum every column.
#
# THE PROBLEM
# ------------
# stdin is a whitespace-separated table of integers. Rows may be ragged
# (a missing cell counts as 0). Print the sum of each column on ONE line,
# separated by single spaces. Empty input prints nothing.
#
#   input:  1 2 3 / 4 5 / 6        (one row per line)
#   output: 11 7 3
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: for each field i, sum[i] += $i; track the max NF; in END join
# sum[1..maxNF] with spaces (unset entries print as 0).
#
# Check with:
#   printf '1 2 3\n4 5\n6\n' | ./sum_columns.sh

awk '{ for (i = 1; i <= NF; i++) sum[i] += $i; if (NF > max) max = NF }
END { if (max > 0) { out = ""; for (i = 1; i <= max; i++) out = out (i > 1 ? " " : "") (sum[i] + 0); print out } }'
