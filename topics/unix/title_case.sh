#!/usr/bin/env bash
#
# Day 30, Task 5 -- Unix/shell: title-case every line.
#
# THE PROBLEM
# ------------
# Read stdin; for every line, uppercase the first letter of each
# whitespace-separated word and lowercase the rest. Keep single spaces
# between words as in the input; blank lines stay blank.
#   hello WORLD foo   ->   Hello World Foo
#   aBC               ->   Abc
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop over fields, $i = toupper(substr($i,1,1)) tolower(substr($i,2)),
# then print $0 (awk re-joins fields with single spaces).
#
# Check with:
#   printf 'hello WORLD foo\naBC\n\nthe quick  brown\n' | ./title_case.sh
# Expected:
#   Hello World Foo
#   Abc
#
#   The Quick Brown

awk '{
    for (i = 1; i <= NF; i++) $i = toupper(substr($i, 1, 1)) tolower(substr($i, 2))
    print $0
}'
