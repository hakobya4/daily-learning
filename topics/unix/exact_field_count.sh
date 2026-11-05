#!/usr/bin/env bash
#
# Day 45, Task 5 -- Unix/shell: lines with exactly N fields, with line numbers.
#
# THE PROBLEM
# ------------
# Usage: ./exact_field_count.sh FILE N
# FILE is split on whitespace. Print "LINENO:line" for every line that has
# exactly N fields (N is a non-negative integer; N=0 matches blank lines).
# At the end print "total: K" where K is the number of lines printed.
# Exit 1 on bad usage, a non-integer N, or an unreadable FILE.
#
# HINT: awk -v n="$2" 'NF==n { print NR ":" $0; k++ } END { print "total: " k+0 }'
#
# Check with:
#   printf 'a b\nc\nd e\n\nf g h\n' > /tmp/d45b; ./exact_field_count.sh /tmp/d45b 2
# Expected:
#   1:a b
#   3:d e
#   total: 2

if [ $# -ne 2 ] || [ ! -r "$1" ] || [ -d "$1" ] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
  echo "usage: $0 FILE N" >&2
  exit 1
fi
awk -v n="$2" 'NF==n { print NR ":" $0; k++ } END { print "total: " k+0 }' "$1"
