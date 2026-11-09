#!/usr/bin/env bash
#
# Day 50, Task 6 -- Unix/shell: Kth line from the end.
#
# THE PROBLEM
# ------------
# Usage: ./kth_line_from_end.sh K FILE
# Print the Kth line counting from the END of FILE (K=1 is the last line). Exit 1 if K
# is not a positive integer, FILE is unreadable, or FILE has fewer than K lines.
#
# HINT: tail -n K | head -n 1, but check the line count first (wc -l / awk END).
#
# Check with:
#   printf 'a\nb\nc\nd\n' > /tmp/d50b
#   ./kth_line_from_end.sh 2 /tmp/d50b
# Expected:
#   c

if [ $# -ne 2 ] || ! [[ "$1" =~ ^[1-9][0-9]*$ ]] || [ ! -r "$2" ] || [ -d "$2" ]; then
  echo "usage: $0 K FILE" >&2
  exit 1
fi

# TODO: replace this line
exit 1
