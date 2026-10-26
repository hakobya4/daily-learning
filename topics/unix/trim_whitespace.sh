#!/usr/bin/env bash
#
# Day 36, Task 6 -- Unix/shell: trim and normalize whitespace.
#
# THE PROBLEM
# ------------
# For every line on stdin: remove leading and trailing spaces/tabs, and
# collapse each internal run of spaces/tabs into a single space. Lines that
# become empty are printed as empty lines (keep them).
#
# Input (· = space, → = tab):
#   ··hello···world··
#   →a→→b→
#   (whitespace only)
# Output:
#   hello world
#   a b
#   (empty line)
#
# HINT: sed -E 's/[ \t]+/ /g; s/^ //; s/ $//'   (write it yourself first;
# awk '{$1=$1}1' is another route).
#
# Check with:
#   printf '  hello   world  \n\ta\t\tb\t\n   \n' | ./trim_whitespace.sh
# Expected:
#   hello world
#   a b
#   (empty line)

# TODO: replace this line
exit 1
