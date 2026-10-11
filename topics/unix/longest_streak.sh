#!/usr/bin/env bash
#
# Day 20, Task 6 -- Unix/shell: longest streak of OK.
#
# THE PROBLEM
# ------------
# stdin has one status per line (OK or FAIL, anything else counts as a
# break just like FAIL). Print the length of the longest run of
# consecutive OK lines. Empty input prints 0.
#
#   input:  OK OK FAIL OK OK OK FAIL   (one per line)
#   output: 3
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: cur = ($0=="OK") ? cur+1 : 0; track max; print it in END.
#
# Check with:
#   printf 'OK\nOK\nFAIL\nOK\nOK\nOK\nFAIL\n' | ./longest_streak.sh

awk '{ cur = ($0 == "OK") ? cur + 1 : 0; if (cur > best) best = cur }
END { print best + 0 }'
