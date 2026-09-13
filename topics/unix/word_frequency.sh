#!/usr/bin/env bash
#
# Day 1, Task 4 -- Unix/shell: word frequency counter.
#
# THE PROBLEM
# ------------
# Given a text file (path passed as $1), print the top 5 most frequent
# words and their counts, one per line, most frequent first. Treat
# words case-insensitively and strip punctuation (make your own file with repeated words).

if [ -z "$1" ]; then
    echo "Usage: $0 <textfile>" >&2
    exit 1
fi

tr 'A-Z' 'a-z' < "$1" | tr -cs 'a-z' '\n' | sort | uniq -c | sort -rn | head -n 5

