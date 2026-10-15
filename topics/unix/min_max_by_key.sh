#!/usr/bin/env bash
#
# Day 25, Task 6 -- Unix/shell: min and max value per key.
#
# THE PROBLEM
# ------------
# stdin has lines "KEY VALUE" (whitespace separated, VALUE is a number,
# possibly negative or decimal). Print one line per key: "KEY MIN MAX",
# sorted by KEY (plain string order). Skip blank lines.
#
#   input:  a 3 / b 5 / a 1 / b 9 / a 2
#   output: a 1 3
#           b 5 9
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk with min[] and max[] arrays: on the first sighting of a key (use
# `!($1 in min)`) set both to $2, otherwise compare numerically (use $2+0).
# Pipe the END output through sort, or sort the keys yourself.
#
# Check with:
#   printf 'a 3\nb 5\na 1\nb 9\na 2\n' | ./min_max_by_key.sh

# TODO: replace this line
echo "not implemented" >&2; exit 1
