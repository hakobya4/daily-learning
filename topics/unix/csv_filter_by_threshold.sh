#!/usr/bin/env bash
#
# Day 48, Task 4 -- Unix/shell: filter CSV rows by a numeric column threshold.
#
# THE PROBLEM
# ------------
# Usage: ./csv_filter_by_threshold.sh FILE COLUMN_NAME THRESHOLD
# FILE is a comma-separated file (no quoted commas) whose first line is a header.
# Print the header, then every row whose COLUMN_NAME value is strictly greater than
# THRESHOLD (numeric comparison, values may be decimals). Keep the original row text.
# Exit 1 on bad usage, unreadable FILE, or if COLUMN_NAME is not in the header.
#
# HINT: awk -F, : find the column index from NR==1, then compare $idx + 0 > t + 0.
#
# Check with:
#   printf 'name,score\nann,9.5\nbob,7\ncy,10\n' > /tmp/d48a
#   ./csv_filter_by_threshold.sh /tmp/d48a score 8
# Expected:
#   name,score
#   ann,9.5
#   cy,10

if [ $# -ne 3 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE COLUMN_NAME THRESHOLD" >&2
  exit 1
fi

# TODO: replace this line
exit 1
