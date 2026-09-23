#!/usr/bin/env bash
#
# Day 3, Task 5 -- Unix/shell: de-duplicate lines, preserving order.
#
# THE PROBLEM
# ------------
# Given a text file (path passed as $1), print its lines with exact
# duplicates removed, keeping only the FIRST occurrence of each line
# and preserving original order. Plain `sort -u` won't work here since
# it reorders lines alphabetically -- that's the point of the
# exercise.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk with an associative "seen" array is the classic one-liner for
# this (`!seen[$0]++`) -- figure out why it works rather than just
# pasting it: what does `seen[$0]++` return the FIRST time a line is
# seen vs every time after?

if [ -z "$1" ]; then
    echo "Usage: $0 <textfile>" >&2
    exit 1
fi

# TODO: replace this line with your implementation.
echo "not implemented" >&2
exit 1
