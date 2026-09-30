#!/usr/bin/env bash
#
# Day 9, Task 6 -- Unix/shell: parse a KEY=VALUE .env file.
#
# THE PROBLEM
# ------------
# $1 is a .env-style file. Print each setting as "KEY -> VALUE", sorted
# by KEY, following these rules:
#   - blank lines and lines starting with '#' (optionally indented) are ignored
#   - leading/trailing spaces around KEY and VALUE are trimmed
#   - only the FIRST '=' splits (a value may itself contain '=')
#   - if a KEY appears twice, the LAST one wins
#
# Test file:
#   # comment
#   NAME = alpha
#   URL=http://x/?a=b
#
#   NAME=beta
# should print exactly:
#   NAME -> beta
#   URL -> http://x/?a=b
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk -F sets a separator but splits on EVERY '='; instead use index($0,"=")
# and substr to split once. Store values in an awk array keyed by KEY so
# later lines overwrite, print in END, and pipe to sort.

if [ -z "$1" ]; then
    echo "Usage: $0 <envfile>" >&2
    exit 1
fi

awk '
function trim(s) { sub(/^[ \t\r]+/, "", s); sub(/[ \t\r]+$/, "", s); return s }
{
    line = trim($0)
    if (line == "" || substr(line, 1, 1) == "#") next
    i = index(line, "=")
    if (i == 0) next
    key = trim(substr(line, 1, i - 1))
    val = trim(substr(line, i + 1))
    if (key == "") next
    vals[key] = val
}
END { for (k in vals) print k " -> " vals[k] }
' "$1" | sort
