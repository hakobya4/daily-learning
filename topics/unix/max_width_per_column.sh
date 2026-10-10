#!/usr/bin/env bash
#
# Day 20, Task 5 -- Unix/shell: maximum width per column.
#
# THE PROBLEM
# ------------
# stdin has whitespace-separated fields; rows may have different numbers
# of fields. For every column (1-based) print "col N: W" where W is the
# length of the longest field in that column. Print columns in order.
#
#   input:  a bbb cc
#           dddd e
#           f g hhhhh
#   output: col 1: 4
#           col 2: 3
#           col 3: 5
#
# Empty input prints nothing.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop i=1..NF, keep w[i] = max(w[i], length($i)), track the largest
# NF seen, and print in an END block.
#
# Check with:
#   printf 'a bbb cc\ndddd e\nf g hhhhh\n' | ./max_width_per_column.sh

# TODO: replace this line
exit 1
