#!/usr/bin/env bash
#
# Day 14, Task 5 -- Unix/shell: join backslash-continued lines.
#
# THE PROBLEM
# ------------
# $1 is a text file. Any line ending in a backslash continues on the
# next line. Print the logical lines: remove the trailing backslash,
# strip the leading whitespace of the continuation line, and join them
# directly (a chain of several continued lines joins into one).
#
#   cc -o app \
#       main.c \
#       util.c
#   echo done
#
# prints:
#   cc -o app main.c util.c
#   echo done
#
# HOW TO WORK THROUGH THIS
# -------------------------
# sed -e :a -e '/\\$/N; s/\\\n[[:space:]]*//; ta' "$1"   (one approach),
# or awk accumulating a buffer while the line ends in "\".
#
# Check with:
#   printf 'a \\\n   b \\\n c\nd\n' > /tmp/j.txt && ./join_continuations.sh /tmp/j.txt
#   -> "a b c" then "d"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>" >&2
    exit 1
fi

awk '
{
    line = $0
    if (cont) sub(/^[ \t]+/, "", line)
    if (line ~ /\\$/) {
        sub(/\\$/, "", line)
        buf = buf line
        cont = 1
    } else {
        print buf line
        buf = ""
        cont = 0
    }
}
END { if (cont) print buf }' "$1"
