#!/usr/bin/env bash
#
# Day 23, Task 5 -- Unix/shell: longest word on each line.
#
# THE PROBLEM
# ------------
# stdin has lines of whitespace-separated words. For EACH input line print
# the longest word on it (the FIRST one if several tie). A line with no
# words prints an empty line.
#
#   input:  the quick brown fox / hi / (empty) / a bb cc
#   output: quick / hi / (empty) / bb
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop i over 1..NF, keep the best with length($i) > length(best)
# (strictly greater keeps the first tie), print it at the end of each line.
#
# Check with:
#   printf 'the quick brown fox\nhi\n\na bb cc\n' | ./longest_word_per_line.sh

awk '{
    best = ""
    for (i = 1; i <= NF; i++)
        if (length($i) > length(best)) best = $i
    print best
}'
