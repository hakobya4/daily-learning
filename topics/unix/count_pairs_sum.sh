#!/usr/bin/env bash
#
# Day 51, Task 4 -- Unix/shell: count pairs that add up to K.
#
# THE PROBLEM
# ------------
# Usage: ./count_pairs_sum.sh K FILE
# FILE holds one integer per line (blank lines ignored). Print how many pairs of DIFFERENT
# lines (i < j) have values that add up to K. Equal values on different lines count as a pair.
# Exit 1 if K is not an integer, or FILE is missing/unreadable.
#
# HINT: one pass with awk and an associative array: before storing x, add seen[K - x]
# to the count; then seen[x]++.
#
# Check with:
#   printf '1\n2\n3\n4\n3\n' > /tmp/d51a
#   ./count_pairs_sum.sh 6 /tmp/d51a
# Expected:
#   2

if [ "$#" -ne 2 ]; then
    echo "usage: $0 K FILE" >&2
    exit 1
fi
k=$1
file=$2
if ! [[ "$k" =~ ^-?[0-9]+$ ]]; then
    echo "error: K must be an integer: $k" >&2
    exit 1
fi
if [ ! -f "$file" ] || [ ! -r "$file" ]; then
    echo "error: cannot read file: $file" >&2
    exit 1
fi

awk -v k="$k" '
    /^[[:space:]]*$/ { next }
    { x = $1 + 0; count += seen[k - x]; seen[x]++ }
    END { print count + 0 }
' "$file"
