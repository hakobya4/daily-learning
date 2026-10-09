#!/usr/bin/env bash
#
# Day 19, Task 6 -- Unix/shell: zero-pad every number in text.
#
# THE PROBLEM
# ------------
# Copy stdin to stdout, but left-pad every run of digits shorter than 4
# digits with zeros to width 4. Runs of 4+ digits stay as they are.
#
#   input:  file1.txt file12.txt v2026
#   output: file0001.txt file0012.txt v2026
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop with match($0, /[0-9]+/), copy the text before the match, the
# padded number (sprintf("%04d") is fine only if you keep leading zeros in
# mind -- numbers like "007" must become "0007"), then continue with the rest.
#
# Check with:
#   printf 'file1.txt file12.txt v2026\n' | ./pad_numbers.sh

# TODO: replace this line
exit 1
