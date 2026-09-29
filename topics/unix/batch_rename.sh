#!/usr/bin/env bash
#
# Day 8, Task 5 -- Unix/shell: batch-rename files with a prefix.
#
# THE PROBLEM
# ------------
# Given a directory ($1) and a prefix string ($2), rename every
# REGULAR FILE directly inside that directory (NOT recursively --
# leave subdirectories and their contents alone) by prepending the
# prefix to its filename -- UNLESS the filename already starts with
# that prefix, in which case leave it untouched. Print one line per
# file actually renamed, in the form:
#   <old path> -> <new path>
#
# That "skip if already prefixed" rule matters: it makes the script
# IDEMPOTENT -- running it a second time with the same arguments
# renames nothing and prints nothing, instead of double-prefixing
# everything.
#
# Make a scratch directory to test against, e.g.:
#   mkdir -p /tmp/rename_test/sub
#   touch /tmp/rename_test/a.txt /tmp/rename_test/b.txt \
#         /tmp/rename_test/sub/c.txt
#   ./batch_rename.sh /tmp/rename_test done_
# should rename a.txt and b.txt to done_a.txt and done_b.txt, print
# both renames, and leave sub/c.txt completely alone. Running the
# exact same command again afterward should rename nothing and print
# nothing.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `find "$1" -maxdepth 1 -type f` lists only regular files directly in
# the directory (maxdepth 1 is what keeps subdirectories out of it).
# For each one, get just the filename with `basename`, check whether
# it already starts with the prefix (a `case` pattern match --
# "$base" matching "$prefix"* -- is a clean, portable way to do a
# starts-with check in bash), and if it doesn't, `mv` it to
# "$1/$prefix$base" and print the old-path/new-path line.

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <directory> <prefix>" >&2
    exit 1
fi

dir="$1"
prefix="$2"

find "$dir" -maxdepth 1 -type f | while IFS= read -r f; do
    base=$(basename "$f")
    case "$base" in
        "$prefix"*) continue ;;
    esac
    mv -- "$f" "$dir/$prefix$base" && echo "$f -> $dir/$prefix$base"
done
