#!/usr/bin/env bash
#
# Day 16, Task 5 -- Unix/shell: fill gaps in a daily series.
#
# THE PROBLEM
# ------------
# stdin has lines "YYYY-MM-DD count", sorted ascending, all in one month
# or spanning several. For every calendar day between the first and the
# last date (inclusive) print "date count"; days missing from the input
# print count 0.
#
#   input:  2026-01-30 5 / 2026-02-02 3
#   output: 2026-01-30 5 / 2026-01-31 0 / 2026-02-01 0 / 2026-02-02 3
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Load the input into an awk array, then loop with GNU `date -d "$d +1 day"`
# from first to last date. Empty input prints nothing.
#
# Check with:
#   printf '2026-01-30 5\n2026-02-02 3\n' | ./fill_missing_dates.sh
#   -> 2026-01-30 5 / 2026-01-31 0 / 2026-02-01 0 / 2026-02-02 3

first=""
declare -A counts
last=""
while read -r d c _; do
    [ -z "$d" ] && continue
    [ -z "$first" ] && first="$d"
    counts[$d]=$(( ${counts[$d]:-0} + c ))
    last="$d"
done
[ -z "$first" ] && exit 0
d="$first"
while :; do
    echo "$d ${counts[$d]:-0}"
    [ "$d" = "$last" ] && break
    d=$(date -d "$d +1 day" +%F)
done
