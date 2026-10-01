#!/usr/bin/env bash
#
# Day 11, Task 4 -- Unix/shell: transpose a CSV.
#
# THE PROBLEM
# ------------
# $1 is a simple CSV (comma-separated, no quoted commas, all rows have
# the same number of fields). Print its transpose: row i of the output
# is column i of the input, comma-separated.
#
# Example input:        Output:
#   a,b,c                 a,1
#   1,2,3                 b,2
#                         c,3
#
# An empty file prints nothing and exits 0.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: store every cell in a 2-D array keyed by (row, col), remember the
# max column count, and print column-major in END. Join with ",".
#
# Check with:  printf 'a,b,c\n1,2,3\n' > /tmp/t.csv && ./transpose_csv.sh /tmp/t.csv

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file.csv>" >&2
    exit 1
fi

# TODO: replace this line
exit 1
