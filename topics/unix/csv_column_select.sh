#!/usr/bin/env bash
#
# Day 7, Task 6 -- Unix/shell: select and reorder CSV columns.
#
# THE PROBLEM
# ------------
# Given a CSV file (path passed as $1, with a header row) and a
# comma-separated list of 1-based column numbers (passed as $2, e.g.
# "3,1"), print the CSV with ONLY those columns, IN THAT ORDER --
# apply the same selection/reorder to every row, including the header.
#
# Make a sample CSV to test against, e.g.:
#   name,score,bonus
#   Alice,10,2
#   Bob,20,5
# Running this script with that file and "3,1" should print:
#   bonus,name
#   2,Alice
#   5,Bob
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk -F, is the tool again. In a BEGIN block, split the $2 argument
# (passed in via -v cols="$2") on ',' into an array with awk's split()
# function -- that gives you the column numbers in the exact order you
# need to print them. Then for EVERY line (header included, so don't
# special-case NR==1 here the way earlier scripts skipped it), loop
# over that array and print $arr[i] for each one, joined with a comma
# (set OFS="," and build up an output line, or just printf pieces with
# a comma between them).

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <csvfile> <column_numbers_comma_separated>" >&2
    exit 1
fi

awk -F, -v cols="$2" '
BEGIN {
    n = split(cols, col_order, ",")
}
{
    line = ""
    for (i = 1; i <= n; i++) {
        if (i > 1) {
            line = line ","
        }
        line = line $(col_order[i])
    }
    print line
}
' "$1"
