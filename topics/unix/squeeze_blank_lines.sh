#!/usr/bin/env bash
#
# Day 22, Task 5 -- Unix/shell: squeeze blank lines.
#
# THE PROBLEM
# ------------
# Read stdin and write it to stdout with these cleanups:
#   * trailing spaces/tabs removed from every line
#   * a run of 2+ blank lines (blank = empty after trimming) collapsed to ONE
#     blank line
#   * leading blank lines and trailing blank lines at the end of the input
#     removed entirely
#
#   input:  "\n\na  \n\n\n\nb\n\n"   (a, 3-line gap, b)
#   output: "a\n\nb\n"
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: strip with sub(/[ \t]+$/, ""); count pending blanks; only print one
# blank line once you see the next non-blank line (and only if you have
# already printed something). Never flush pending blanks in END.
#
# Check with:
#   printf '\n\na  \n\n\n\nb\n\n' | ./squeeze_blank_lines.sh   # a, blank, b

awk '{ sub(/[ \t]+$/, "") }
/^$/ { blanks++; next }
{ if (printed && blanks) print ""; blanks = 0; print; printed = 1 }'
