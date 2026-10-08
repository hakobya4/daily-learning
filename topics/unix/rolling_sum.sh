#!/usr/bin/env bash
#
# Day 17, Task 5 -- Unix/shell: rolling sum over a window of 3.
#
# THE PROBLEM
# ------------
# stdin has one number per line (integers or decimals). For every line
# from the 3rd onward, print the sum of that line and the two before it.
# Lines 1 and 2 print nothing. Fewer than 3 lines -> no output.
#
#   input:  1 2 3 4 5 (one per line)
#   output: 6 / 9 / 12
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: keep the previous two values in variables (or a small array indexed
# by NR % 3) and print when NR >= 3. Print with "%g" or plain print.
#
# Check with:
#   printf '1\n2\n3\n4\n5\n' | ./rolling_sum.sh     -> 6 9 12
#   printf '1.5\n2.5\n3\n' | ./rolling_sum.sh       -> 7

awk 'NF { n++; v[n] = $1; if (n >= 3) print v[n] + v[n-1] + v[n-2] }' 
