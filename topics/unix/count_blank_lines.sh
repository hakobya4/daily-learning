#!/usr/bin/env bash
#
# Day 35, Task 6 -- Unix/shell: count blank vs non-blank lines.
#
# THE PROBLEM
# ------------
# stdin is arbitrary text. Print exactly two lines:
#   blank=<n>
#   nonblank=<m>
# A line is "blank" if it is empty or contains only spaces/tabs.
# Empty input prints blank=0 and nonblank=0.
#
# Input:
#   hello
#
#      
#   world
# (the 3rd line is spaces only)
# Output:
#   blank=2
#   nonblank=2
#
# HINT: awk '/^[ \t]*$/{b++;next}{n++} END{print "blank=" b+0; print "nonblank=" n+0}'
# (try writing it yourself first; grep -c is another route).
#
# Check with:
#   printf 'hello\n\n   \nworld\n' | ./count_blank_lines.sh
# Expected:
#   blank=2
#   nonblank=2

# TODO: replace this line
exit 1
