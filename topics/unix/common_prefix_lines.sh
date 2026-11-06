#!/usr/bin/env bash
#
# Day 46, Task 4 -- Unix/shell: longest common prefix of all lines.
#
# THE PROBLEM
# ------------
# Usage: ./common_prefix_lines.sh FILE
# Print the longest string that every line of FILE starts with (possibly
# empty -> print an empty line). An empty FILE prints an empty line.
# Exit 1 on bad usage or an unreadable FILE.
#
# HINT: take the first line as the candidate prefix and shrink it
# (${p%?}) until every other line matches [[ $line == "$p"* ]]; or use awk.
#
# Check with:
#   printf 'flower\nflow\nflight\n' > /tmp/d46a; ./common_prefix_lines.sh /tmp/d46a
# Expected:
#   fl

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi
p=""
first=1
while IFS= read -r line || [ -n "$line" ]; do
  if [ $first -eq 1 ]; then
    p=$line
    first=0
    continue
  fi
  while [[ $line != "$p"* ]]; do
    p=${p%?}
  done
done < "$1"
printf '%s\n' "$p"
