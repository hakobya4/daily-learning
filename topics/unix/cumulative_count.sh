#!/usr/bin/env bash
#
# Day 28, Task 6 -- Unix/shell: running count of each word's occurrences.
#
# THE PROBLEM
# ------------
# Read one word per line from stdin. For every line print the word, a TAB,
# and how many times that word has appeared SO FAR (including this line).
#
#   input:   a b a c a b
#   output:  a<TAB>1  b<TAB>1  a<TAB>2  c<TAB>1  a<TAB>3  b<TAB>2   (one per line)
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk with an associative array: seen[$1]++ then print $1 "\t" seen[$1].
#
# Check with:
#   printf 'a\nb\na\nc\na\nb\n' | ./cumulative_count.sh
# Expected:
#   a	1
#   b	1
#   a	2
#   c	1
#   a	3
#   b	2

# TODO: replace this line
exit 1
