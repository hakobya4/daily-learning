#!/usr/bin/env bash
#
# Day 1, Task 5 -- Unix/shell: find + grep combo.
#
# THE PROBLEM
# ------------
# Given a directory ($1) and a search term ($2), print the paths of
# every file under that directory that was MODIFIED IN THE LAST 7 DAYS
# and CONTAINS the search term.
#


if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <directory> <search-term>" >&2
    exit 1
fi

find "$1" -type f -mtime -7 -exec grep -l "$2" {} +

