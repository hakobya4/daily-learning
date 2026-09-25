#!/usr/bin/env bash
#
# Day 4, Task 6 -- Unix/shell: find large files.
#
# THE PROBLEM
# ------------
# Given a directory path ($1) and a size threshold in kilobytes ($2),
# recursively find every FILE (not directory) under that path whose
# size is greater than the threshold, and print them largest-first,
# each with a human-readable size.
#
# Make a test directory with a few files of different sizes (e.g.
# `dd`, or just some copies of existing files) to try this against.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `find "$1" -type f -size +"$2"k` gets you the matching files.
# Pipe that into `du -h` (one file at a time, or via -exec/xargs) to
# get human-readable sizes, then `sort -rh` to sort by that
# human-readable size, largest first. `du -h` output is
# "<size>\t<path>" -- `sort -rh` understands human sizes like "12K"
# or "3.4M" directly, no need to convert to raw bytes yourself.

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <directory> <size_threshold_kb>" >&2
    exit 1
fi

find "$1" -type f -size +"$2"k -exec du -h {} \; | sort -rh
