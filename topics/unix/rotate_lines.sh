#!/usr/bin/env bash
#
# Day 52, Task 4 -- Unix/shell: rotate the lines of a file left by K.
#
# THE PROBLEM
# ------------
# Usage: ./rotate_lines.sh FILE K
# Print the lines of FILE rotated LEFT by K: the first K lines move to the end, order
# otherwise preserved. K may be larger than the number of lines (use K mod line-count),
# K = 0 prints the file unchanged, and an empty file prints nothing.
# Exit 1 (usage message on stderr) if the argument count is wrong, FILE is not a readable
# regular file, or K is not a non-negative integer.
#
# HINT: count lines with wc -l (or awk NR), then tail -n +$((k+1)) and head -n "$k"; or a
# single awk that buffers lines and prints from index k+1 around to k. Watch the
# empty-file case (mod by zero).
#
# Check with:
#   printf 'a\nb\nc\nd\ne\n' > /tmp/d52a
#   ./rotate_lines.sh /tmp/d52a 2      # and also try K=7, which gives the same result
# Expected:
#   c
#   d
#   e
#   a
#   b

if [ "$#" -ne 2 ] || [ ! -f "$1" ] || [ ! -r "$1" ] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "usage: $0 FILE K   (K must be a non-negative integer)" >&2
    exit 1
fi

# TODO: replace this line
exit 1
