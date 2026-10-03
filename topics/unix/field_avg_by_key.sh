#!/usr/bin/env bash
#
# Day 12, Task 4 -- Unix/shell: average a numeric column per key.
#
# THE PROBLEM
# ------------
# $1 is a CSV with a header line "key,value". For each distinct key print
#   <key> <average>
# one per line, sorted by key (plain byte order), average with exactly
# 2 decimals. Skip the header. Ignore blank lines.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk with -F, and two associative arrays (sum[key], n[key]); in END
# printf "%s %.2f\n"; pipe to sort (LC_ALL=C sort).
#
# Check with:  printf 'key,value\nb,1\na,2\nb,2\na,5\n' | ./field_avg_by_key.sh /dev/stdin
#              -> "a 3.50" and "b 1.50"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>" >&2
    exit 1
fi

awk -F',' '
    NR == 1 { next }
    NF < 2 || $1 == "" { next }
    { sum[$1] += $2; n[$1]++ }
    END { for (k in sum) printf "%s %.2f\n", k, sum[k] / n[k] }
' "$1" | LC_ALL=C sort
