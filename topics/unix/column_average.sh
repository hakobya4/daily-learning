#!/usr/bin/env bash
#
# Day 49, Task 4 -- Unix/shell: average of a numeric column, grouped by another column.
#
# THE PROBLEM
# ------------
# Usage: ./column_average.sh FILE
# FILE is comma-separated with NO header: group,value  (value is a number, may be decimal).
# Print one line per group: "group avg" where avg has exactly 2 decimals, groups sorted
# alphabetically (LC_ALL=C). Skip blank lines. Exit 1 on bad usage or unreadable FILE.
#
# HINT: awk with sum[$1]+=$2 and cnt[$1]++, printf "%s %.2f\n" in END, pipe to sort.
#
# Check with:
#   printf 'b,4\na,1\nb,5\na,2.5\nc,7\n' > /tmp/d49a
#   ./column_average.sh /tmp/d49a
# Expected:
#   a 1.75
#   b 4.50
#   c 7.00

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi

# TODO: replace this line
exit 1
