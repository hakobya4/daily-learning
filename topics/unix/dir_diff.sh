#!/usr/bin/env bash
#
# Day 5, Task 6 -- Unix/shell: diff two directory listings.
#
# THE PROBLEM
# ------------
# Given two directory paths ($1 and $2), print three sections in this
# order:
#   "Only in $1:" followed by the relative paths of files that exist
#     only under the first directory,
#   "Only in $2:" followed by the relative paths that exist only
#     under the second,
#   "In both:" followed by the relative paths that exist under both
#     (regardless of whether their CONTENTS match -- presence only).
# Compare by path RELATIVE to each directory (e.g. "sub/file.txt"),
# not by full absolute path.
#
# Make two test directories that share a few files and each have a
# few unique ones to try this against.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `(cd "$1" && find . -type f | sort)` gets you the first side's file
# list as sorted relative paths (same trick for $2). Save each to a
# temp file, then `comm -23`, `comm -13`, and `comm -12` on the two
# sorted lists give you "only in first", "only in second", and "in
# both" respectively.

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <dir1> <dir2>" >&2
    exit 1
fi

# TODO: replace this line with your implementation.
echo "not implemented" >&2
exit 1
