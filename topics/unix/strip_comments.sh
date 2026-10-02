#!/usr/bin/env bash
#
# Day 11, Task 5 -- Unix/shell: strip comments and blank lines.
#
# THE PROBLEM
# ------------
# $1 is a config file. Print it with:
#   - everything from the first '#' to end of line removed,
#   - trailing whitespace trimmed from each line,
#   - lines that end up empty dropped.
# (Leading whitespace is kept.) Line order is preserved.
#
# Example:   "port = 80   # http"  ->  "port = 80"
#            "# whole-line"        ->  (dropped)
#            "   "                 ->  (dropped)
#
# HOW TO WORK THROUGH THIS
# -------------------------
# One sed pipeline does it: delete the comment, trim trailing blanks,
# then delete empty lines. (sed -e ... -e ... or two sed calls.)
#
# Check with:  printf 'a=1 # x\n# c\n\n  b=2  \n' | ./strip_comments.sh /dev/stdin
#              -> "a=1" and "  b=2"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>" >&2
    exit 1
fi

sed -e 's/#.*$//' -e 's/[[:space:]]*$//' -e '/^$/d' "$1"
