#!/usr/bin/env bash
#
# Day 37, Task 5 -- Unix/shell: swap the first and last column of a CSV.
#
# THE PROBLEM
# ------------
# stdin is a CSV (comma-separated, NO quoting, every line has the same
# number of columns, at least 2). Print every line (header included) with
# the first and last columns swapped.
#
# Input:
#   id,name,city
#   1,ann,paris
#   2,bob,rome
# Output:
#   city,name,id
#   paris,ann,1
#   rome,bob,2
#
# HINT: awk -F, -v OFS=, '{ t=$1; $1=$NF; $NF=t; print }'
#
# Check with:
#   printf 'id,name,city\n1,ann,paris\n2,bob,rome\n' | ./swap_columns_csv.sh
# Expected:
#   city,name,id
#   paris,ann,1
#   rome,bob,2

# TODO: replace this line
exit 1
