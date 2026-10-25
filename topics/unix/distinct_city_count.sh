#!/usr/bin/env bash
#
# Day 34, Task 6 -- Unix/shell: count distinct values of a CSV column.
#
# THE PROBLEM
# ------------
# stdin is a CSV with a header line (no quoted commas). Print a single
# number: how many DISTINCT values appear in column 2 across the data rows
# (skip the header). Empty input or header-only input prints 0.
#
# Input:
#   name,city
#   ann,Rome
#   bob,Oslo
#   cy,Rome
# Output:
#   2
#
# HINT: awk -F, 'NR>1 && !seen[$2]++ {n++} END {print n+0}'  (try writing it
# yourself first, or use tail -n +2 | cut -d, -f2 | sort -u | wc -l).
#
# Check with:
#   printf 'name,city\nann,Rome\nbob,Oslo\ncy,Rome\n' | ./distinct_city_count.sh
# Expected:
#   2

awk -F, 'NR > 1 && !seen[$2]++ { n++ } END { print n + 0 }'
