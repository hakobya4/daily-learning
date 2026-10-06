#!/usr/bin/env bash
#
# Day 15, Task 5 -- Unix/shell: reverse the order of fields on each line.
#
# THE PROBLEM
# ------------
# Read lines from stdin; print each line with its whitespace-separated
# fields in reverse order, joined by a single space. Blank lines stay
# blank.
#
#   one two three   -> three two one
#   solo            -> solo
#   a   b           -> b a
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop i from NF down to 1, build the output with a separator that
# is empty before the first printed field.
#
# Check with:
#   printf 'one two three\nsolo\n\na   b\n' | ./reverse_fields.sh
#   -> three two one / solo / (blank) / b a

awk '{
    out = ""
    for (i = NF; i >= 1; i--) out = out (out == "" ? "" : " ") $i
    print out
}'
