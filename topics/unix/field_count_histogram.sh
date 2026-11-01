#!/usr/bin/env bash
#
# Day 42, Task 4 -- Unix/shell: histogram of fields-per-line.
#
# THE PROBLEM
# ------------
# Read text on stdin. For every distinct number of whitespace-separated
# fields per line (blank lines count as 0), print "<nf> <count>", sorted by
# nf ascending numerically. Empty input prints nothing.
#
# HINT: awk { c[NF]++ } END { for (k in c) print k, c[k] } piped to sort -n.
#
# Check with:
#   printf 'a b\n\nc\nd e\nf g h\n' | ./field_count_histogram.sh
# Expected:
#   0 1
#   1 1
#   2 2
#   3 1

# TODO: replace this line
exit 1
