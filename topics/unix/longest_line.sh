#!/usr/bin/env bash
#
# Day 10, Task 4 -- Unix/shell: find the longest line in a file.
#
# THE PROBLEM
# ------------
# $1 is a text file. Print the LINE NUMBER and LENGTH of its longest
# line as "<lineno> <length>". If several lines tie, report the first.
# An empty file prints nothing and exits 0.
#
# Example: lines "hi", "hello world", "abc" -> "2 11"
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk's length() and NR do the heavy lifting: track the max and the line
# number where it was first seen, print in END.

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>" >&2
    exit 1
fi

# TODO: replace this line
exit 1
