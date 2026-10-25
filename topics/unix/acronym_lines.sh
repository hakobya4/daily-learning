#!/usr/bin/env bash
#
# Day 34, Task 5 -- Unix/shell: acronym of every line.
#
# THE PROBLEM
# ------------
# stdin is lines of words separated by whitespace. For every line print the
# acronym: the first letter of each word, upper-cased, with no separators.
# A blank line prints a blank line.
#
# Input:
#   portable network graphics
#   say what you mean
#
#   a
# Output:
#   PNG
#   SWYM
#
#   A
#
# HINT: awk, loop i from 1..NF and append toupper(substr($i,1,1)) to a string.
#
# Check with:
#   printf 'portable network graphics\nsay what you mean\n\na\n' | ./acronym_lines.sh
# Expected:
#   PNG
#   SWYM
#
#   A

awk '{ s = ""; for (i = 1; i <= NF; i++) s = s toupper(substr($i, 1, 1)); print s }'
