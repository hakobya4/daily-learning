#!/usr/bin/env bash
#
# Day 31, Task 5 -- Unix/shell: classify years as leap or common.
#
# THE PROBLEM
# ------------
# stdin has one year per line. Print "YEAR leap" or "YEAR common".
# A year is a leap year if it is divisible by 4, except century years,
# which must be divisible by 400.
#   2024 -> 2024 leap      1900 -> 1900 common
#   2000 -> 2000 leap      2023 -> 2023 common
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: ($1 % 4 == 0 && $1 % 100 != 0) || $1 % 400 == 0, then printf with a
# ternary. Skip blank lines (NF == 0).
#
# Check with:
#   printf '1900\n2000\n2024\n2023\n2100\n' | ./leap_years.sh
# Expected:
#   1900 common
#   2000 leap
#   2024 leap
#   2023 common
#   2100 common

# TODO: replace this line (hint: awk 'NF { ... }')
echo "not implemented" >&2; exit 1
