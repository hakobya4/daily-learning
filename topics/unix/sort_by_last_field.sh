#!/usr/bin/env bash
#
# Day 40, Task 5 -- Unix/shell: sort lines by their last field.
#
# THE PROBLEM
# ------------
# Read lines on stdin; fields are separated by whitespace and lines may have
# different numbers of fields. Output the lines (unchanged) sorted by their
# LAST field, numerically ascending. Ties keep input order (stable). Blank
# lines are dropped.
#
# HINT: awk can print the last field ($NF) and the line number in front,
# then `sort -g -s -k1,1`, then `cut` the helper columns away. Or decorate
# with tab characters. Remember sort -s for stability.
#
# Check with:
#   printf 'a b 10\nc 2\nd e f 2\n\ng 1\n' | ./sort_by_last_field.sh
# Expected:
#   g 1
#   c 2
#   d e f 2
#   a b 10

awk 'NF { printf "%s\t%d\t%s\n", $NF, NR, $0 }' \
  | sort -g -s -t "$(printf '\t')" -k1,1 \
  | cut -f3-
