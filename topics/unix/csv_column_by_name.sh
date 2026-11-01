#!/usr/bin/env bash
#
# Day 42, Task 5 -- Unix/shell: select a CSV column by header name.
#
# THE PROBLEM
# ------------
# Usage: ./csv_column_by_name.sh COLNAME < file.csv
# The first line of stdin is a comma-separated header. Print the values of the
# column called COLNAME (without the header), one per line. No quoted commas
# to worry about. If COLNAME is not in the header, print
# "no such column: COLNAME" to stderr and exit 2.
#
# HINT: awk -F, -v col="$1"; on NR==1 loop i over fields to find idx.
#
# Check with:
#   printf 'id,name,age\n1,ann,30\n2,bo,25\n' | ./csv_column_by_name.sh name
# Expected:
#   ann
#   bo
#   printf 'id,name\n1,x\n' | ./csv_column_by_name.sh zip   -> exit code 2

# TODO: replace this line
exit 1
