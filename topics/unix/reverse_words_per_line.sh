#!/usr/bin/env bash
#
# Day 45, Task 4 -- Unix/shell: reverse the order of words on each line.
#
# THE PROBLEM
# ------------
# Usage: ./reverse_words_per_line.sh FILE
# For every line of FILE print its whitespace-separated words in reverse order,
# joined by single spaces. Blank lines stay blank. Exit 1 on bad usage or an
# unreadable FILE.
#
# HINT: awk '{ s=""; for (i=NF; i>=1; i--) s = s (s=="" ? "" : " ") $i; print s }'
#
# Check with:
#   printf 'one two three\n\nsolo\n  a   b  \n' > /tmp/d45a; ./reverse_words_per_line.sh /tmp/d45a
# Expected:
#   three two one
#
#   solo
#   b a

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi
awk '{ s=""; for (i=NF; i>=1; i--) s = s (s=="" ? "" : " ") $i; print s }' "$1"
