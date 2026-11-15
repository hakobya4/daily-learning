#!/usr/bin/env bash
#
# Day 55, Task 4 -- Unix/shell: extract one column from a CSV with QUOTED fields.
#
# THE PROBLEM
# ------------
# Usage: ./csv_quoted_column.sh N FILE
# Print field number N (1-based) of every line of FILE, where FILE is CSV in the RFC 4180
# style restricted to single-line records:
#   * fields are separated by commas;
#   * a field MAY be wrapped in double quotes, in which case it can contain commas;
#   * inside a quoted field, a doubled quote "" stands for one literal quote character.
# Output the UNQUOTED value (outer quotes removed, "" turned into ").
# A line with fewer than N fields prints an empty line (keep line alignment).
# Exit 1 with a usage message on stderr if the argument count is wrong, N is not a positive
# integer, or FILE is not a readable regular file.
# Exit 2 with "line L: unterminated quote" on stderr (L = 1-based line number) as soon as a
# line ends while still inside a quoted field (lines before it are still printed).
#
# HINT: `cut -d,` and plain `awk -F,` both split inside quotes -- that is the trap.
# Walk each line character by character in awk with a tiny state machine:
#   in_quotes = 0; field = 1; value = ""
#   for each char c: if in_quotes: '"' followed by '"' -> append '"' and skip one,
#   lone '"' -> in_quotes = 0, else append c.  Outside quotes: '"' -> in_quotes = 1,
#   ',' -> field++, else append c (only while field == N).
# (GNU awk's FPAT is an alternative, but write the portable state machine.)
#
# Check with:
#   printf '%s\n' 'id,name,comment' '1,"Smith, Ana","said ""hi"""' '2,Bo,plain' \
#     '3,"",x' '4' '5,"a,b,c",' > /tmp/d55.csv
#   ./csv_quoted_column.sh 2 /tmp/d55.csv
# Expected:
#   name
#   Smith, Ana
#   Bo
#   (an empty line for the "" field)
#   (an empty line for the 1-field line "4")
#   a,b,c
#   ./csv_quoted_column.sh 3 /tmp/d55.csv
# Expected:
#   comment
#   said "hi"
#   plain
#   x
#   (empty)
#   (empty)
#   printf '%s\n' 'a,b' '"open,c' 'never printed' > /tmp/d55bad.csv
#   ./csv_quoted_column.sh 1 /tmp/d55bad.csv; echo "exit=$?"
# Expected stdout: a  then  exit=2   (stderr: line 2: unterminated quote)

usage() {
    echo "usage: $0 N FILE   (N = 1-based column number)" >&2
    exit 1
}

[ "$#" -eq 2 ] || usage
case "$1" in
    ''|*[!0-9]*|0*) usage ;;          # must be a positive integer without leading zeros
esac
[ -f "$2" ] && [ -r "$2" ] || usage

# Character-by-character state machine: commas inside quotes do not split fields,
# and "" inside a quoted field is one literal quote.
awk -v n="$1" '
{
    line = $0
    len = length(line)
    inq = 0; field = 1; val = ""
    for (i = 1; i <= len; i++) {
        c = substr(line, i, 1)
        if (inq) {
            if (c == "\"") {
                if (substr(line, i + 1, 1) == "\"") {   # escaped quote
                    if (field == n) val = val "\""
                    i++
                } else {
                    inq = 0                             # closing quote
                }
            } else if (field == n) {
                val = val c
            }
        } else if (c == "\"") {
            inq = 1
        } else if (c == ",") {
            field++
        } else if (field == n) {
            val = val c
        }
    }
    if (inq) {
        printf "line %d: unterminated quote\n", NR > "/dev/stderr"
        exit 2
    }
    print val
}' "$2"
