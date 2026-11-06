#!/usr/bin/env bash
#
# Day 46, Task 5 -- Unix/shell: second largest DISTINCT number.
#
# THE PROBLEM
# ------------
# Usage: ./second_largest.sh FILE
# FILE has one integer per line (may be negative, may repeat). Print the
# second largest distinct value. If there are fewer than 2 distinct values
# print "none". Exit 1 on bad usage or an unreadable FILE.
#
# HINT: sort -n -u | tail -n 2 | head -n 1 (then check the count), or one awk pass
# tracking max and second.
#
# Check with:
#   printf '5\n9\n9\n-2\n7\n' > /tmp/d46b; ./second_largest.sh /tmp/d46b
# Expected:
#   7

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi
awk 'NF { print $1 + 0 }' "$1" | sort -n -u | awk '{ a[NR] = $0 } END { if (NR < 2) print "none"; else print a[NR-1] }'
