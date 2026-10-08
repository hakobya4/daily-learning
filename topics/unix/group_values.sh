#!/usr/bin/env bash
#
# Day 17, Task 6 -- Unix/shell: group values by key.
#
# THE PROBLEM
# ------------
# stdin has lines "key value" (whitespace separated, value has no spaces).
# Print one line per distinct key, in order of FIRST appearance, as
# "key: v1,v2,v3" with the values in input order. Skip blank lines.
#
#   input:  a 1 / b 2 / a 3 / c 4 / b 5
#   output: a: 1,3 / b: 2,5 / c: 4
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk with an associative array vals[key] plus an `order` array that
# records each new key once; print in END.
#
# Check with:
#   printf 'a 1\nb 2\na 3\nc 4\nb 5\n' | ./group_values.sh
#   -> a: 1,3 / b: 2,5 / c: 4

awk 'NF >= 2 {
  if (!($1 in vals)) { order[++n] = $1; vals[$1] = $2 }
  else vals[$1] = vals[$1] "," $2
}
END { for (i = 1; i <= n; i++) print order[i] ": " vals[order[i]] }' 
