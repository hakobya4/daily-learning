#!/usr/bin/env bash
#
# Day 53, Task 4 -- Unix/shell: lines of A that never appear in B (order-preserving set difference).
#
# THE PROBLEM
# ------------
# Usage: ./set_difference.sh FILE_A FILE_B
# Print every line of FILE_A that does NOT appear anywhere in FILE_B (whole-line, exact
# match), keeping FILE_A's original order and printing each such line only ONCE (its first
# occurrence). FILE_B may be empty (then print A's distinct lines in order).
# Exit 1 (usage message on stderr) if the argument count is wrong or either file is not a
# readable regular file.
#
# HINT: `comm -23` needs sorted input and loses the original order -- avoid it. The classic
# two-file awk idiom: while reading the first file given to awk (NR == FNR) remember its
# lines in an array; for the second file print lines that are not in it and not yet seen.
# Watch out: if FILE_B is empty, NR == FNR is also true for FILE_A -- use FILENAME instead.
#
# Check with:
#   printf 'apple\nbanana\ncherry\napple\ndate\ncherry\negg\n' > /tmp/d53a
#   printf 'banana\ndate\nfig\n' > /tmp/d53b
#   ./set_difference.sh /tmp/d53a /tmp/d53b
# Expected:
#   apple
#   cherry
#   egg
# And with an empty B:  : > /tmp/d53e; ./set_difference.sh /tmp/d53b /tmp/d53e
# Expected:
#   banana
#   date
#   fig

if [ "$#" -ne 2 ] || [ ! -f "$1" ] || [ ! -r "$1" ] || [ ! -f "$2" ] || [ ! -r "$2" ]; then
    echo "usage: $0 FILE_A FILE_B" >&2
    exit 1
fi

# TODO: replace this line
exit 1
