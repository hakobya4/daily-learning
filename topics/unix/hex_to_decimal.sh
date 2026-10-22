#!/usr/bin/env bash
#
# Day 32, Task 5 -- Unix/shell: hex to decimal.
#
# THE PROBLEM
# ------------
# stdin has one token per line. If the token is a valid hexadecimal number
# (optional 0x/0X prefix, then 1+ hex digits, either case) print its decimal
# value. Otherwise print the word invalid. Skip blank lines.
#   ff      -> 255
#   0x1A    -> 26
#   10      -> 16
#   xyz     -> invalid
#   0x      -> invalid
#
# HOW TO WORK THROUGH THIS
# -------------------------
# A bash while-read loop with a regex test ([[ $line =~ ^(0[xX])?[0-9a-fA-F]+$ ]])
# and printf '%d' "0x..." works; strip the prefix first so "10" is hex 10.
#
# Check with:
#   printf 'ff\n0x1A\n10\nxyz\n0x\n' | ./hex_to_decimal.sh
# Expected:
#   255
#   26
#   16
#   invalid
#   invalid

# TODO: replace this line
exit 1
