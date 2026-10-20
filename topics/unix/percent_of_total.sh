#!/usr/bin/env bash
#
# Day 30, Task 6 -- Unix/shell: percentage of total per row.
#
# THE PROBLEM
# ------------
# stdin has lines "name number". Print each line as "name number pct" where
# pct is that number's share of the grand total, with one decimal and a %
# sign, keeping the input order. Needs two passes over the data.
#   a 1
#   b 3     ->   a 1 25.0%
#                b 3 75.0%
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: store lines and values in arrays while summing, then loop in the END
# block with printf "%s %s %.1f%%\n". (Total is 0? Not in the tests.)
#
# Check with:
#   printf 'a 1\nb 3\n' | ./percent_of_total.sh
# Expected:
#   a 1 25.0%
#   b 3 75.0%

# TODO: replace this line
echo "not implemented" >&2; exit 1
