#!/usr/bin/env bash
#
# Day 49, Task 5 -- Unix/shell: collapse adjacent duplicate lines with a repeat count.
#
# THE PROBLEM
# ------------
# Usage: ./dedupe_adjacent.sh FILE
# Read FILE and, for each run of identical CONSECUTIVE lines, print the line once,
# followed by " x<N>" only if the run length N is greater than 1. Non-adjacent repeats
# are separate runs. Preserve order. Exit 1 on bad usage or unreadable FILE.
#
# HINT: awk keeping prev and count; flush on change and in END. (Not the same as sort -u.)
#
# Check with:
#   printf 'a\na\nb\na\nc\nc\nc\n' > /tmp/d49b
#   ./dedupe_adjacent.sh /tmp/d49b
# Expected:
#   a x2
#   b
#   a
#   c x3

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi

# TODO: replace this line
exit 1
