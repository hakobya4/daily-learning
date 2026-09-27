#!/usr/bin/env bash
#
# Day 6, Task 5 -- Unix/shell: merge sorted files into one sorted stream.
#
# THE PROBLEM
# ------------
# Given two or more file paths ($1, $2, ...), each ALREADY sorted
# line-by-line, print a single merged output that is ALL of their
# lines combined, still in overall sorted order -- without just
# concatenating and re-sorting everything from scratch (that works,
# but defeats the point: `sort -m` merges pre-sorted inputs in linear
# time instead of re-sorting the whole thing).
#
# Make 2-3 small sorted text files to test against, e.g.:
#   file_a.txt: apple, mango, zebra
#   file_b.txt: banana, kiwi, yak
# Merged output should be: apple, banana, kiwi, mango, yak, zebra
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `sort -m "$@"` does exactly this: -m tells sort to MERGE its inputs,
# assuming each is already sorted, instead of re-sorting from
# scratch. "$@" passes along every argument given to this script. Look
# up why plain `sort -m` on files with different sort orders (e.g. one
# case-sensitive, one not) can give a subtly wrong merged result --
# mention it in a comment once you understand it.

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <sorted_file1> <sorted_file2> [more_sorted_files...]" >&2
    exit 1
fi

sort -m "$@"
# Note: plain `sort -m` assumes every input file was already sorted
# using the SAME collation/sort order that this `sort` invocation
# would use by default (locale-dependent, e.g. LC_COLLATE). If one
# file was pre-sorted case-sensitively (byte order, so "Zebra" sorts
# before "apple") and another was pre-sorted case-insensitively (or
# under a different locale), merging them with `sort -m` silently
# produces a subtly wrong interleaving -- `-m` only merges, it never
# re-sorts, so it trusts each input's existing order instead of
# verifying it.
