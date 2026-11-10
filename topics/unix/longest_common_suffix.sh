#!/usr/bin/env bash
#
# Day 50, Task 5 -- Unix/shell: longest common suffix of all lines.
#
# THE PROBLEM
# ------------
# Usage: ./longest_common_suffix.sh FILE
# Print the longest string that every line of FILE ends with (an empty line if there is
# none, or if FILE is empty). Exit 1 on bad usage or unreadable FILE.
#
# HINT: reverse each line with rev, find the common PREFIX, then rev the result.
#
# Check with:
#   printf 'running\njumping\nsing\n' > /tmp/d50a
#   ./longest_common_suffix.sh /tmp/d50a
# Expected:
#   ing

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi

if [ ! -s "$1" ]; then
  echo
  exit 0
fi
rev "$1" | awk '
  NR == 1 { p = $0; next }
  {
    n = (length(p) < length($0)) ? length(p) : length($0)
    i = 1
    while (i <= n && substr(p, i, 1) == substr($0, i, 1)) i++
    p = substr(p, 1, i - 1)
  }
  END { print p }' | rev
