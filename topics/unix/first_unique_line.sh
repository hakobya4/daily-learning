#!/usr/bin/env bash
#
# Day 32, Task 6 -- Unix/shell: first line that occurs exactly once.
#
# THE PROBLEM
# ------------
# stdin has arbitrary text lines. Print the FIRST line (in input order)
# whose exact text appears only once in the whole input. If every line is
# repeated, print nothing.
#   a b a c b   (one per line)  -> c
#   x x y y                      -> (nothing)
#   p q r                        -> p
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Needs two passes over the data: awk can store every line in an array and
# count occurrences in an associative array, then loop in order in END.
#
# Check with:
#   printf 'a\nb\na\nc\nb\n' | ./first_unique_line.sh
# Expected:
#   c

awk '{ lines[NR] = $0; count[$0]++ }
     END { for (i = 1; i <= NR; i++) if (count[lines[i]] == 1) { print lines[i]; exit } }'
