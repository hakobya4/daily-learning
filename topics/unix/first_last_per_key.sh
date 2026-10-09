#!/usr/bin/env bash
#
# Day 19, Task 5 -- Unix/shell: first and last value per key.
#
# THE PROBLEM
# ------------
# stdin lines are "key value" (whitespace separated). Print one line per key,
# "key first last", where first/last are the first and last values seen for
# that key. Keys appear in first-appearance order. A key seen once prints
# the same value twice.
#
#   input:  a 1 / b 5 / a 7 / a 9
#   output: a 1 9 / b 5 5
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: on a new key, record order[++n] = key and first[key]; always set
# last[key] = $2; loop 1..n in END.
#
# Check with:
#   printf 'a 1\nb 5\na 7\na 9\n' | ./first_last_per_key.sh

# TODO: replace this line
exit 1
