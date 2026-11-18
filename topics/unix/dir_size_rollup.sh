#!/usr/bin/env bash
#
# Day 58, Task 5 -- Unix/shell: roll file sizes up into per-directory totals (like du).
#
# THE PROBLEM
# ------------
# Usage: ./dir_size_rollup.sh DEPTH FILE
# FILE lists files, one per line: "SIZE PATH" -- SIZE is a byte count (all digits),
# PATH is a RELATIVE file path ("a/b/c.txt"). A valid line has exactly 2 fields, SIZE
# matches ^[0-9]+$, and PATH does not start or end with "/" and contains no empty
# component ("a//b") and no "." or ".." component. Other lines are skipped and
# counted.
# Print the total size of every DIRECTORY whose depth is <= DEPTH, where the
# top-level directories ("a") have depth 1, "a/b" depth 2, and so on; a directory's
# total includes every file anywhere below it. The first line is always the grand total
# for "." (all valid files, including files directly at the top level).
# Output format: "TOTAL<TAB>DIR", "." first, then the directories sorted by path in
# plain byte order (LC_ALL=C sort). Directories that only exist deeper than DEPTH are
# not printed; a file's own name is never printed. Finally print "skipped K" to
# STDERR (always).
# Exit 1 with a usage message on stderr if the argument count is wrong, DEPTH is not a
# positive integer (no leading zeros), or FILE is not a readable regular file.
#
# HINT: in awk, for each valid line split($2, parts, "/"); the file's directories are
# the prefixes parts[1], parts[1]"/"parts[2], ... up to n-1 components (never the
# file name itself) -- add the size to each prefix whose depth <= DEPTH, building the
# prefix incrementally. Print "." in END, and pipe the directory lines through sort.
# Validate PATH with a regex: no leading/trailing "/", no "//", and test each
# component against "." and "..".
#
# Check with:
#   printf '%s\n' '100 a/x.txt' '200 a/b/y.txt' '50 a/b/c/z.txt' '10 top.txt' \
#     '300 d/e/f.bin' 'bad line' '-5 a/q' '20 /abs/path' '7 a//b.txt' '1 a/./k' \
#     '5 a/b' '3 extra field here' > /tmp/d58.files
#   ./dir_size_rollup.sh 2 /tmp/d58.files
# Expected stdout (TAB-separated):
#   665     .
#   355     a
#   250     a/b
#   300     d
#   300     d/e
# Expected stderr:
#   skipped 6
#   ./dir_size_rollup.sh 1 /tmp/d58.files  -> ".", "a" (355) and "d" (300) only
#   ./dir_size_rollup.sh 02 /tmp/d58.files -> usage message, exit 1

usage() {
    echo "usage: $0 DEPTH FILE   (DEPTH: positive integer, FILE: readable regular file of \"SIZE PATH\" lines)" >&2
    exit 1
}

[ "$#" -eq 2 ] || usage
depth=$1
file=$2
[[ $depth =~ ^[1-9][0-9]*$ ]] || usage
[ -f "$file" ] && [ -r "$file" ] || usage

awk -v maxd="$depth" '
function valid_path(path,    n, parts, i) {
    if (path ~ /^\// || path ~ /\/$/ || path ~ /\/\//) return 0
    n = split(path, parts, "/")
    for (i = 1; i <= n; i++)
        if (parts[i] == "" || parts[i] == "." || parts[i] == "..") return 0
    return 1
}
{
    if (NF != 2 || $1 !~ /^[0-9]+$/ || !valid_path($2)) { skipped++; next }
    size = $1 + 0
    total += size
    n = split($2, parts, "/")
    prefix = ""
    # directories are the first n-1 components; never the file name itself
    for (i = 1; i < n && i <= maxd; i++) {
        prefix = (i == 1) ? parts[1] : prefix "/" parts[i]
        sum[prefix] += size
    }
}
END {
    printf "%d\t.\n", total
    fflush()
    cmd = "LC_ALL=C sort -k2,2"
    for (d in sum) printf "%d\t%s\n", sum[d], d | cmd
    close(cmd)
    print "skipped " (skipped + 0) > "/dev/stderr"
}' "$file"
