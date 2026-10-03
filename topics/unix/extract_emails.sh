#!/usr/bin/env bash
#
# Day 12, Task 5 -- Unix/shell: extract unique email addresses.
#
# THE PROBLEM
# ------------
# $1 is a free-form text file. Print every email address found in it,
# lower-cased, one per line, sorted and de-duplicated. An address is
# [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,} ; trailing punctuation
# such as a final "." or "," that is not part of the match must not
# appear in the output.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# grep -Eo prints only the matching parts; then tr to lower-case, then
# LC_ALL=C sort -u.
#
# Check with:  printf 'Mail Bob@Example.com, or ann.l@x.org.\nbob@example.com\n' | ./extract_emails.sh /dev/stdin
#              -> "ann.l@x.org" and "bob@example.com"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>" >&2
    exit 1
fi

grep -Eo '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$1" | tr '[:upper:]' '[:lower:]' | LC_ALL=C sort -u
