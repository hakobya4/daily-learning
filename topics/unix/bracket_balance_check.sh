#!/usr/bin/env bash
#
# Day 38, Task 6 -- Unix/shell: check bracket balance per line.
#
# THE PROBLEM
# ------------
# Read stdin; for each line print "<line number>:OK" if its (), [] and {}
# are balanced and correctly nested (other characters are ignored), else
# "<line number>:BAD". An empty line is OK.
#
# Input (stdin):
#   (a[b]{c})
#   (]
#   ((
#   <empty>
#
# Output:
#   1:OK
#   2:BAD
#   3:BAD
#   4:OK
#
# HINT: awk with a manual stack array, iterating characters via substr().
#
# Check with:
#   printf '(a[b]{c})\n(]\n((\n\n' | ./bracket_balance_check.sh
# Expected:
#   1:OK
#   2:BAD
#   3:BAD
#   4:OK

# TODO: replace this line
exit 1
