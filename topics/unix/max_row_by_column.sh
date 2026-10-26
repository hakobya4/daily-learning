#!/usr/bin/env bash
#
# Day 35, Task 5 -- Unix/shell: print the row with the maximum value in column 3.
#
# THE PROBLEM
# ------------
# stdin is a comma-separated file with a header line. Column 3 holds
# integers. Print the header, then ONLY the data row whose column 3 is the
# largest (if several tie, print the first one). Header-only or empty input
# prints just the header (or nothing for empty input).
#
# Input:
#   name,team,score
#   ann,red,7
#   bob,blue,12
#   cy,red,12
# Output:
#   name,team,score
#   bob,blue,12
#
# HINT: awk -F, 'NR==1{print;next} NR==2||$3>m{m=$3;r=$0} END{if(r!="")print r}'
# (try writing it yourself first).
#
# Check with:
#   printf 'name,team,score\nann,red,7\nbob,blue,12\ncy,red,12\n' | ./max_row_by_column.sh
# Expected:
#   name,team,score
#   bob,blue,12

awk -F, 'NR==1{print;next} NR==2||$3+0>m+0{m=$3;r=$0} END{if(r!="")print r}'
