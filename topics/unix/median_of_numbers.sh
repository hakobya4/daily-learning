#!/usr/bin/env bash
#
# Day 39, Task 4 -- Unix/shell: median of numbers on stdin.
#
# THE PROBLEM
# ------------
# Read numbers from stdin, one per line (integers or decimals, may be
# negative, unsorted). Print their median. For an even count, the median is
# the average of the two middle values. Print with awk's "%g" style (so 2.0
# prints as 2 and 2.5 prints as 2.5). Empty input prints nothing.
#
# HINT: sort -g | awk '{a[NR]=$1} END {...}' -- pick a[(NR+1)/2] for odd NR,
# average a[NR/2] and a[NR/2+1] for even NR.
#
# Check with:
#   printf '3\n1\n2\n' | ./median_of_numbers.sh        # Expected: 2
#   printf '4\n1\n3\n2\n' | ./median_of_numbers.sh     # Expected: 2.5
#   printf -- '-5\n10\n' | ./median_of_numbers.sh      # Expected: 2.5
#   printf '7\n' | ./median_of_numbers.sh              # Expected: 7

sort -g | awk '
  { a[NR] = $1 }
  END {
    if (NR == 0) exit 0
    if (NR % 2) printf "%g\n", a[(NR + 1) / 2]
    else printf "%g\n", (a[NR / 2] + a[NR / 2 + 1]) / 2
  }'
