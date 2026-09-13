#!/usr/bin/env bash
#
# Day 2, Task 8 -- Unix/shell: find + grep combo.
#
# THE PROBLEM
# ------------
# Given a directory ($1) and a search term ($2), print the paths of
# every file under that directory that was MODIFIED IN THE LAST 7 DAYS
# and CONTAINS the search term.
#
# This practices combining `find` (filter by metadata: recency) with
# `grep` (filter by content) -- two different filtering axes chained
# together, which is a very common real-world Unix pattern (e.g.
# "which recently-touched log files mention this error?").
#
# Useful building blocks:
#   find <dir> -type f -mtime -7     -- files modified in the last 7 days
#   grep -l "<term>" <files...>      -- print only filenames that match
#   find ... -exec grep -l "<term>" {} +   -- chain them directly
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Try `find` alone first and confirm it lists what you expect, THEN
# add the grep step -- debugging one filter at a time beats guessing
# at a combined command.
#
# Test with: ./find_recent_matches.sh . "TODO"
# (should find files in this repo that were touched recently and
# contain the word TODO -- there should be plenty right now)

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <directory> <search-term>" >&2
    exit 1
fi

# TODO: replace the line below with your real find+grep command.
echo "TODO: not implemented yet"
