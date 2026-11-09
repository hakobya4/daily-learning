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

# TODO: replace this line
exit 1
