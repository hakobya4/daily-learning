#!/usr/bin/env bash
#
# Day 25, Task 5 -- Unix/shell: histogram of word lengths.
#
# THE PROBLEM
# ------------
# stdin is free text. Split it on whitespace into words. Print one line per
# distinct word length, "LENGTH COUNT" (space-separated), sorted by LENGTH
# ascending (numerically). Empty input prints nothing.
#
#   input:  a bb cc ddd a
#   output: 1 2
#           2 2
#           3 1
#
# HOW TO WORK THROUGH THIS
# -------------------------
# tr -s '[:space:]' '\n' to one word per line, drop empty lines, awk
# '{ print length($0) }', then sort -n | uniq -c and reformat (uniq -c puts
# the count first, so swap the columns). Or do it all in awk with an array.
#
# Check with:
#   printf 'a bb cc ddd a\n' | ./word_length_histogram.sh

# TODO: replace this line
echo "not implemented" >&2; exit 1
