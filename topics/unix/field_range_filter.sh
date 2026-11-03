#!/usr/bin/env bash
#
# Day 44, Task 5 -- Unix/shell: filter lines by numeric range of field 2.
#
# THE PROBLEM
# ------------
# Usage: ./field_range_filter.sh FILE LO HI
# FILE has whitespace-separated fields. Print every line whose 2nd field is
# an integer with LO <= value <= HI (inclusive). Lines with fewer than 2
# fields or a non-integer 2nd field are skipped. Exit 1 on bad usage or an
# unreadable FILE.
#
# HINT: awk -v lo="$2" -v hi="$3" '$2 ~ /^-?[0-9]+$/ && $2+0 >= lo && $2+0 <= hi'
#
# Check with:
#   printf 'a 5\nb 10\nc 15\nd x\ne\n' > /tmp/d44b; ./field_range_filter.sh /tmp/d44b 5 10
# Expected:
#   a 5
#   b 10

# TODO: replace this line
exit 1
