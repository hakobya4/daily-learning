#!/usr/bin/env bash
#
# Day 37, Task 6 -- Unix/shell: print a line range with line numbers.
#
# THE PROBLEM
# ------------
# $1 = N, $2 = M (1-based, N <= M). Read stdin and print lines N through M
# inclusive, each prefixed by its original line number and a colon
# (e.g. "3:foo"). Lines outside the range are not printed. If the input
# is shorter than N, print nothing.
#
# Input (stdin):  a b c d e   (one per line)   with args 2 4
# Output:
#   2:b
#   3:c
#   4:d
#
# HINT: awk -v n="$1" -v m="$2" 'NR>=n && NR<=m {print NR ":" $0}'
#
# Check with:
#   printf 'a\nb\nc\nd\ne\n' | ./lines_between_n_m.sh 2 4
# Expected:
#   2:b
#   3:c
#   4:d

awk -v n="$1" -v m="$2" 'NR>=n && NR<=m {print NR ":" $0}'
