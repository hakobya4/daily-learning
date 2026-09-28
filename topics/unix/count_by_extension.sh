#!/usr/bin/env bash
#
# Day 7, Task 5 -- Unix/shell: count files by extension.
#
# THE PROBLEM
# ------------
# Given a directory ($1), recursively count REGULAR FILES under it,
# grouped by extension (the part of the filename after its LAST '.'),
# and print one line per extension as:
#   <count> <extension>
# sorted highest count first. A file with no '.' in its name at all
# counts under the literal bucket name "noext" (not blank, not skipped).
#
# Make a scratch directory with a mix of files to test against, e.g.:
#   mkdir -p /tmp/ext_test/sub
#   touch /tmp/ext_test/a.txt /tmp/ext_test/b.txt /tmp/ext_test/sub/c.py \
#         /tmp/ext_test/README /tmp/ext_test/sub/d.txt
#   ./count_by_extension.sh /tmp/ext_test
# should print (order among equal counts doesn't matter):
#   3 txt
#   1 py
#   1 noext
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `find "$1" -type f` lists every regular file, full path and all.
# Strip each path down to just the filename (basename, or a shell
# parameter expansion like ${path##*/}), then decide the extension:
# if the filename contains a '.', it's everything after the LAST one
# (${filename##*.}); if it doesn't contain a '.' at all, use "noext".
# Tally counts per extension (an awk associative array is the natural
# fit here, same pattern as log_level_summary.sh from Day 3), then
# print sorted by count descending -- `sort -rn` on the final
# "<count> <extension>" lines works once they're in that order.

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

find "$1" -type f | awk -F/ '
{
    filename = $NF
    if (index(filename, ".") > 0) {
        n = split(filename, parts, ".")
        ext = parts[n]
    } else {
        ext = "noext"
    }
    counts[ext]++
}
END {
    for (ext in counts) {
        print counts[ext], ext
    }
}
' | sort -rn
