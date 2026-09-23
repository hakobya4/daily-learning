#!/usr/bin/env bash
#
# Day 3, Task 4 -- Unix/shell: log level summary.
#
# THE PROBLEM
# ------------
# Given a log file (path passed as $1) where each line starts with a
# level tag like "ERROR", "WARN", or "INFO", print a count of lines
# for EACH level, sorted highest count first, in the form:
#   <count> <LEVEL>
#
# Make your own sample log file with a mix of levels to test against,
# e.g.:
#   ERROR something broke
#   INFO all good
#   WARN disk getting full
#   ERROR something else broke
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk on the first field is the cleanest tool here -- pull field 1 off
# each line, tally with an associative array, print at END. A pure
# pipeline (cut/sort/uniq -c/sort) also works if you'd rather practice
# that instead.

if [ -z "$1" ]; then
    echo "Usage: $0 <logfile>" >&2
    exit 1
fi

# TODO: replace this line with your implementation.
echo "not implemented" >&2
exit 1
