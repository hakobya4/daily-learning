#!/usr/bin/env bash
#
# Day 4, Task 5 -- Unix/shell: sum a CSV column.
#
# THE PROBLEM
# ------------
# Given a CSV file (path passed as $1, with a header row) and a
# 1-based column number (passed as $2), print the sum of that
# column's numeric values across all DATA rows (skip the header).
#
# Make your own sample CSV to test against, e.g.:
#   name,score,bonus
#   Alice,10,2
#   Bob,20,5
#   Carol,30,1
# Running this script with that file and column 2 should print 60.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk -F, is the tool here: skip the header with NR>1, pull out field
# number $2 (the column argument) using an awk variable passed in via
# -v, and tally a running sum in an END block. Don't hardcode which
# field number to use inside the awk program -- read it from $2.

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <csvfile> <column_number>" >&2
    exit 1
fi

awk -F, -v col="$2" 'NR > 1 { sum += $col } END { print sum }' "$1"
