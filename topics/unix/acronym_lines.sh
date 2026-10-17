#!/usr/bin/env bash
#
# Day 27, Task 6 -- Unix/shell: make an uppercase acronym from each line.
#
# THE PROBLEM
# ------------
# For every line on stdin print the uppercase first letters of its
# whitespace-separated words. Blank lines produce blank lines.
#
#   input:  portable network graphics
#   output: PNG
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop i from 1 to NF, append toupper(substr($i, 1, 1)) to a string,
# print it (even if empty) at the end of each record.
#
# Check with:
#   printf 'portable network graphics\nas soon as possible\n\nhello\n' | ./acronym_lines.sh
# Expected:
#   PNG
#   ASAP
#
#   H

# TODO: replace this line
exit 1
