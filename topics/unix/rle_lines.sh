#!/usr/bin/env bash
#
# Day 16, Task 6 -- Unix/shell: collapse runs of identical lines.
#
# THE PROBLEM
# ------------
# stdin is any text. Print each run of CONSECUTIVE identical lines once,
# prefixed by the run length and a tab: "<count>\t<line>". Non-adjacent
# repeats are separate runs (unlike `sort | uniq -c`, order is preserved).
#
#   input:  a / a / b / a / a / a
#   output: 2<TAB>a / 1<TAB>b / 3<TAB>a
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `uniq -c` pads with spaces, so either reformat its output with sed/awk,
# or do it all in awk keeping `prev` and `n`. Don't forget the last run.
#
# Check with:
#   printf 'a\na\nb\na\na\na\n' | ./rle_lines.sh | cat -A
#   -> 2^Ia$ / 1^Ib$ / 3^Ia$

# TODO: replace this line
exit 1
