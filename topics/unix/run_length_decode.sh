#!/usr/bin/env bash
#
# Day 53, Task 5 -- Unix/shell: decode run-length tokens line by line.
#
# THE PROBLEM
# ------------
# Usage: ./run_length_decode.sh FILE
# Each line of FILE holds space-separated tokens of the form COUNT CHAR glued together, e.g.
# "3a" means "aaa". The LAST character of a token is CHAR (any non-space character, even a
# digit or punctuation) and everything before it is COUNT, a positive integer that may have
# several digits: "12z" = twelve z's, "2-" = "--", "35" = "555".
# For every line print the decoded tokens concatenated with no separator.
# A blank line prints a blank line. If any token is malformed (no count, or count 0), print
# "bad token: TOKEN (line N)" to stderr and exit 2 immediately.
# Exit 1 (usage message on stderr) if the argument count is wrong or FILE is not readable.
#
# HINT: awk: for each field, ch = substr($i, length($i)); n = substr($i, 1, length($i)-1);
# validate n with a regex like /^[1-9][0-9]*$/, then append ch n times in a loop. Exit
# status from awk: `exit 2` inside awk, then `exit $?` (or let it be the script's last
# command).
#
# Check with:
#   printf '3a 2b 1c\n1x 4-\n\n12z\n35 1!\n' > /tmp/d53r
#   ./run_length_decode.sh /tmp/d53r
# Expected:
#   aaabbc
#   x----
#
#   zzzzzzzzzzzz
#   555!
# And: printf 'ok 2a\n' > /tmp/d53bad; ./run_length_decode.sh /tmp/d53bad; echo "rc=$?"
# Expected (stderr then stdout):
#   bad token: ok (line 1)
#   rc=2

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

awk '
{
    out = ""
    for (i = 1; i <= NF; i++) {
        tok = $i
        ch = substr(tok, length(tok))
        n = substr(tok, 1, length(tok) - 1)
        if (n !~ /^[1-9][0-9]*$/) {
            printf "bad token: %s (line %d)\n", tok, NR > "/dev/stderr"
            exit 2
        }
        for (j = 0; j < n + 0; j++) out = out ch
    }
    print out
}
' "$1"
