#!/usr/bin/env bash
#
# Day 44, Task 4 -- Unix/shell: sum of digit characters per line.
#
# THE PROBLEM
# ------------
# Usage: ./sum_digits_per_line.sh FILE
# For every line of FILE print the sum of its individual digit characters
# (non-digits are ignored; a line without digits gives 0, empty lines too).
# Exit 1 with a message on stderr if FILE is not readable.
#
# HINT: awk with split($0, ch, "") and a numeric test, or
#       sed 's/[^0-9]/ /g' ... or fold -w1 per line.
#
# Check with:
#   printf 'abc123\n\n9x9\n007\n' > /tmp/d44a; ./sum_digits_per_line.sh /tmp/d44a
# Expected:
#   6
#   0
#   18
#   7

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE (readable)" >&2
  exit 1
fi
awk '{ s = 0; n = split($0, ch, ""); for (i = 1; i <= n; i++) if (ch[i] ~ /[0-9]/) s += ch[i]; print s }' "$1"
