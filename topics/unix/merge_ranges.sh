#!/usr/bin/env bash
#
# Day 23, Task 6 -- Unix/shell: merge integer ranges.
#
# THE PROBLEM
# ------------
# stdin has one range per line, formatted A-B (non-negative integers,
# A <= B), in any order. Print the merged ranges sorted ascending, one per
# line as A-B. Ranges that OVERLAP or share an endpoint are merged
# (start <= current end); ranges that merely sit side by side, like 1-3 and
# 4-6, stay separate.
#
#   input:  5-8 / 1-3 / 2-4 / 10-12 / 8-9
#   output: 1-4 / 5-9 / 10-12
#
# HOW TO WORK THROUGH THIS
# -------------------------
# sort numerically by start (sort -t- -k1,1n), then one awk pass keeping the
# current [s,e]: if the next start <= e extend e to max(e, next end), else
# print the current range and start a new one. Print the last at END.
#
# Check with:
#   printf '5-8\n1-3\n2-4\n10-12\n8-9\n' | ./merge_ranges.sh

sort -t- -k1,1n | awk -F- '
NF >= 2 {
    a = $1 + 0; b = $2 + 0
    if (!have) { s = a; e = b; have = 1 }
    else if (a <= e) { if (b > e) e = b }
    else { print s "-" e; s = a; e = b }
}
END { if (have) print s "-" e }
'
