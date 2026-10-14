#!/usr/bin/env bash
#
# Day 24, Task 5 -- Unix/shell: count files per extension.
#
# THE PROBLEM
# ------------
# stdin has one file path per line. Print "<count> <ext>" for each distinct
# extension, sorted by count descending, then extension ascending. The
# extension is the lowercase text after the LAST dot in the file NAME (the
# part after the last '/'). Files with no dot, or only a leading dot
# (".bashrc"), count under the extension "(none)".
#
#   input:  src/a.PY / src/b.py / README / docs/x.tar.gz / .bashrc / lib/c.py
#   output: 3 py / 2 (none) / 1 gz     (one per line, count first)
#
# HOW TO WORK THROUGH THIS
# -------------------------
# strip the directory (awk -F/ '{print $NF}'), then use awk to find the
# last dot (match / index tricks, or split on "." and take $NF when NF > 1
# and the first field is non-empty), tolower() it, count in an array, and
# finish with: sort -k1,1nr -k2,2
#
# Check with:
#   printf 'src/a.PY\nsrc/b.py\nREADME\ndocs/x.tar.gz\n.bashrc\nlib/c.py\n' | ./extension_counts.sh

# TODO: replace this line
exit 1
