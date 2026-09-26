#!/usr/bin/env bash
#
# Day 5, Task 5 -- Unix/shell: find duplicate files by content.
#
# THE PROBLEM
# ------------
# Given a directory path ($1), recursively find files that are exact
# duplicates of each other BY CONTENT (not by name) -- two files with
# different names but identical bytes count as duplicates. Print each
# group of duplicates together, separated by a blank line, one full
# file path per line. A file with no duplicate anywhere under the
# directory should not be printed at all.
#
# Make a test directory with a couple of duplicate files (e.g. `cp`
# one file to a second name) plus a few unique ones to try this
# against.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `find "$1" -type f -exec sha256sum {} +` gives you a
# "<hash>  <path>" line per file. Sort those lines by hash so equal
# hashes end up adjacent, then walk them (awk works well here) to
# group consecutive lines sharing a hash -- only print a group once it
# has 2 or more members.

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

find "$1" -type f -exec sha256sum {} + \
    | sort \
    | awk '
        function flush() {
            if (count >= 2) {
                if (printed_any) {
                    print ""
                }
                printf "%s", buffer
                printed_any = 1
            }
        }
        {
            hash = $1
            path = $0
            sub(/^[^ ]+ +/, "", path)
            if (hash != prev_hash) {
                flush()
                buffer = ""
                count = 0
            }
            buffer = buffer path "\n"
            count++
            prev_hash = hash
        }
        END { flush() }
    '

