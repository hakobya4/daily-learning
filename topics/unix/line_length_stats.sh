#!/usr/bin/env bash
#
# Day 47, Task 5 -- Unix/shell: line-length statistics.
#
# THE PROBLEM
# ------------
# Usage: ./line_length_stats.sh FILE
# Print one line: min=<shortest> max=<longest> avg=<mean>, measured in characters
# over ALL lines (empty lines count as length 0). avg has exactly 2 decimals.
# If FILE has no lines print "none". Exit 1 on bad usage or an unreadable FILE.
#
# HINT: one awk pass: track min/max/sum with length($0), printf "%.2f" in END.
#
# Check with:
#   printf 'ab\nabcd\nabc\n' > /tmp/d47b; ./line_length_stats.sh /tmp/d47b
# Expected:
#   min=2 max=4 avg=3.00

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi
awk '{ l = length($0); if (NR == 1 || l < mn) mn = l; if (NR == 1 || l > mx) mx = l; sum += l }
  END { if (NR == 0) print "none"; else printf "min=%d max=%d avg=%.2f\n", mn, mx, sum / NR }' "$1"
