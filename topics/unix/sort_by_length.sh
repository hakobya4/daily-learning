#!/usr/bin/env bash
#
# Day 21, Task 5 -- Unix/shell: sort lines by length.
#
# THE PROBLEM
# ------------
# stdin has one string per line. Print the lines sorted by length
# (shortest first); lines of equal length are sorted alphabetically
# (byte order, i.e. LC_ALL=C). Empty input prints nothing.
#
#   input:  pear fig apple kiwi fig2   (one per line)
#   output: fig, fig2, kiwi, pear, apple   (one per line)
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Prefix each line with its length (awk), sort numerically on that and
# then on the line with LC_ALL=C sort, then cut the prefix off again.
#
# Check with:
#   printf 'pear\nfig\napple\nkiwi\nfig2\n' | ./sort_by_length.sh

# TODO: replace this line
exit 1
