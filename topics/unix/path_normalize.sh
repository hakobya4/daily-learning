#!/usr/bin/env bash
#
# Day 60, Task 5 -- Unix/shell: normalize file paths lexically (no filesystem access).
#
# THE PROBLEM
# ------------
# Usage: ./path_normalize.sh [-b BASE] [FILE]        (reads stdin when FILE is omitted)
# Each input line is one path. Print each path normalized PURELY LEXICALLY (never look
# at the disk, never use realpath/readlink -f/python):
#   - runs of "/" collapse to one ("a//b" -> "a/b"); a leading "//" is just "/";
#   - "." segments are dropped;
#   - ".." removes the previous real segment; at the root of an ABSOLUTE path it is
#     dropped ("/../a" -> "/a"); in a RELATIVE path with nothing left to remove it is
#     KEPT ("../../a" stays, "a/../../b" -> "../b");
#   - a trailing "/" is removed (except for "/" itself);
#   - an empty relative result prints "." ("a/.." -> ".").
# With -b BASE (BASE must start with "/"), every RELATIVE input path is first joined
# as BASE/path and then normalized; absolute inputs ignore BASE.
# An empty line prints "line N: empty path" to STDERR (N = input line number) and
# nothing on stdout; processing continues and the exit status stays 0.
# Exit 2 with a usage line on stderr if BASE is missing / not absolute, there are
# extra arguments, or FILE is not a readable regular file.
#
# HINT: one awk program: split($0, parts, "/"), push segments onto a stack array
# (skip "" and ".", pop on ".." when the top is a real segment, otherwise keep ".." for
# relative paths), then join with "/" and prefix "/" if the input started with "/".
# Spaces inside path segments must survive, so treat the whole line as one path
# (don't let awk split it on whitespace -- use $0, not $1).
#
# Check with:
#   printf '%s\n' '/usr//local/./bin/' 'a/b/../c' '../../x/./y/..' '/../etc/' \
#     'a/..' '' './my docs//notes.txt' '//srv///www/' '.' 'a/../../b' > /tmp/p.txt
#   ./path_normalize.sh /tmp/p.txt; echo "exit=$?"
# Expected stdout:
#   /usr/local/bin
#   a/c
#   ../../x
#   /etc
#   .
#   my docs/notes.txt
#   /srv/www
#   .
#   ../b
#   exit=0
# Expected stderr:
#   line 6: empty path
#   printf '%s\n' 'src/../lib' '/tmp/x' '../up' | ./path_normalize.sh -b /home/narek/proj
#     -> /home/narek/proj/lib
#        /tmp/x
#        /home/narek/up
#   ./path_normalize.sh -b relative/base /tmp/p.txt   -> usage on stderr, exit 2

usage() {
    echo "usage: $(basename "$0") [-b BASE] [FILE]   (BASE must be absolute)" >&2
    exit 2
}

base=""
have_base=0
while getopts ":b:" opt; do
    case "$opt" in
        b) base="$OPTARG"; have_base=1 ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))

if [ "$have_base" -eq 1 ] && [ "${base#/}" = "$base" ]; then
    usage
fi
[ $# -le 1 ] || usage
if [ $# -eq 1 ]; then
    { [ -f "$1" ] && [ -r "$1" ]; } || usage
    input="$1"
else
    input="-"
fi

awk -v base="$base" '
{
    path = $0
    sub(/\r$/, "", path)
    if (path == "") {
        printf "line %d: empty path\n", NR > "/dev/stderr"
        next
    }
    if (base != "" && substr(path, 1, 1) != "/")
        path = base "/" path
    abs = (substr(path, 1, 1) == "/")
    n = split(path, parts, "/")
    top = 0
    for (k = 1; k <= n; k++) {
        seg = parts[k]
        if (seg == "" || seg == ".") continue
        if (seg == "..") {
            if (top > 0 && stack[top] != "..") { top--; continue }
            if (abs) continue
        }
        stack[++top] = seg
    }
    out = ""
    for (k = 1; k <= top; k++) out = (k == 1 ? stack[k] : out "/" stack[k])
    if (abs) out = "/" out
    else if (out == "") out = "."
    print out
}' "$input"
