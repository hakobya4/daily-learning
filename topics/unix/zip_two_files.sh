#!/usr/bin/env bash
#
# Day 43, Task 5 -- Unix/shell: zip two files line by line.
#
# THE PROBLEM
# ------------
# Usage: ./zip_two_files.sh FILE1 FILE2
# Print line i of FILE1 and line i of FILE2 joined by a colon: "l1:l2".
# Stop when the SHORTER file ends (extra lines of the longer file are ignored).
# Exit 1 with a message on stderr if either file is not readable.
#
# HINT: paste -d: pads the shorter side with empty fields, so either trim the
#       output to min(wc -l) lines with head -n, or use awk with
#       `getline line < file2` and stop when it returns <= 0.
#
# Check with:
#   printf 'a\nb\nc\n' > /tmp/f1; printf '1\n2\n' > /tmp/f2
#   ./zip_two_files.sh /tmp/f1 /tmp/f2
# Expected:
#   a:1
#   b:2
#   ./zip_two_files.sh /tmp/f1 /nonexistent   -> exit code 1

# TODO: replace this line
exit 1
