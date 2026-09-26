#!/usr/bin/env bash
#
# Day 6, Task 6 -- Unix/shell: extract lines between two markers.
#
# THE PROBLEM
# ------------
# Given a text file (path passed as $1), a START marker string ($2),
# and an END marker string ($3), print every line from the FIRST line
# containing the start marker through the FIRST line AFTER it
# containing the end marker (inclusive of both marker lines). If there
# are multiple start/end pairs in the file, only handle the first one
# -- don't worry about repeats.
#
# Make a test file with a block you want to pull out, e.g. marked by
# "-- BEGIN --" and "-- END --" lines, to try this against.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk's range pattern is built for exactly this: `/start/,/end/` as a
# pattern (with no action) prints every line from the first match of
# `start` through the next match of `end`, inclusive. Pass $2 and $3
# in as awk variables (-v start="$2" -v end="$3") and build the range
# pattern from those variables rather than hardcoding text, since awk
# patterns don't directly interpolate shell variables.

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Usage: $0 <file> <start_marker> <end_marker>" >&2
    exit 1
fi

# TODO: replace this line with your implementation.
echo "not implemented" >&2
exit 1
