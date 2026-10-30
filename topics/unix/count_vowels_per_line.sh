#!/usr/bin/env bash
#
# Day 40, Task 4 -- Unix/shell: vowels per line.
#
# THE PROBLEM
# ------------
# Read text on stdin. For every line print "<line number>:<vowel count>"
# (line numbers start at 1). Vowels are a e i o u in either case; y does not
# count. Empty lines print "N:0".
#
# HINT: awk: gsub(/[aeiouAEIOU]/, "&") returns the number of substitutions.
# Do not modify the line before printing -- count on a copy.
#
# Check with:
#   printf 'Hello World\n\nSky\nAUDIO\n' | ./count_vowels_per_line.sh
# Expected:
#   1:3
#   2:0
#   3:0
#   4:4

# TODO: replace this line
exit 1
