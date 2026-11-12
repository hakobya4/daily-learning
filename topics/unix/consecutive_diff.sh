#!/usr/bin/env bash
#
# Day 52, Task 5 -- Unix/shell: differences between consecutive numbers.
#
# THE PROBLEM
# ------------
# Usage: ./consecutive_diff.sh FILE
# FILE holds one integer per line (possibly negative). Blank lines are skipped. For every
# number after the first, print "<previous> -> <current>: <current - previous>", one per line.
# A file with fewer than two numbers prints nothing. Exit 1 on bad usage or unreadable FILE.
#
# HINT: awk with a "have previous" flag (don't test prev == "" -- 0 is a valid value);
# skip lines matching /^[[:space:]]*$/.
#
# Check with:
#   printf '3\n7\n\n7\n2\n-4\n10\n' > /tmp/d52b
#   ./consecutive_diff.sh /tmp/d52b
# Expected:
#   3 -> 7: 4
#   7 -> 7: 0
#   7 -> 2: -5
#   2 -> -4: -6
#   -4 -> 10: 14

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

awk '
    /^[[:space:]]*$/ { next }
    {
        cur = $1 + 0
        if (have) printf "%d -> %d: %d\n", prev, cur, cur - prev
        prev = cur
        have = 1
    }
' "$1"
