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

# TODO: replace this line
exit 1
