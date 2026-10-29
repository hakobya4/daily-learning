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

awk '
{
  top = 0; ok = 1
  n = length($0)
  for (i = 1; i <= n && ok; i++) {
    c = substr($0, i, 1)
    if (c == "(" || c == "[" || c == "{") {
      stack[++top] = c
    } else if (c == ")" || c == "]" || c == "}") {
      if (top == 0) { ok = 0; break }
      o = stack[top--]
      if (!((o == "(" && c == ")") || (o == "[" && c == "]") || (o == "{" && c == "}"))) ok = 0
    }
  }
  if (top != 0) ok = 0
  print NR ":" (ok ? "OK" : "BAD")
}'
