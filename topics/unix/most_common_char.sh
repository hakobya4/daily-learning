#!/usr/bin/env bash
#
# Day 33, Task 6 -- Unix/shell: most common non-whitespace character.
#
# THE PROBLEM
# ------------
# stdin has arbitrary text. Ignoring all whitespace (spaces, tabs,
# newlines), print the character that occurs most often, a space, and its
# count: "<char> <count>". If several characters tie, print the one that
# sorts first in byte (C locale) order. Empty input prints nothing.
#   hello world   -> l 3
#   aabb          -> a 2        (tie: a before b)
#   (empty)       -> (nothing)
#
# HINT: `fold -w1` (or `grep -o .`) puts one character per line; then
# count with `sort | uniq -c`, and order with sort -k1,1nr -k2,2 under
# LC_ALL=C. Remember to drop whitespace first (tr -d '[:space:]').
#
# Check with:
#   printf 'hello world\n' | ./most_common_char.sh
# Expected:
#   l 3

# TODO: replace this line
exit 1
