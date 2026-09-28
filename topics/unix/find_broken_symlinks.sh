#!/usr/bin/env bash
#
# Day 8, Task 6 -- Unix/shell: find broken symbolic links.
#
# THE PROBLEM
# ------------
# Given a directory ($1), recursively find every SYMBOLIC LINK under
# it whose target does NOT exist (a "broken" symlink), and print each
# broken link's own path, one per line, sorted alphabetically. A
# symlink pointing at another symlink that eventually resolves to a
# real file is NOT broken; only ones whose target is genuinely
# missing count.
#
# Make a scratch directory to test against, e.g.:
#   mkdir -p /tmp/symlink_test/sub
#   touch /tmp/symlink_test/real.txt
#   ln -s /tmp/symlink_test/real.txt /tmp/symlink_test/good_link
#   ln -s /tmp/symlink_test/nope.txt /tmp/symlink_test/bad_link
#   ln -s /tmp/symlink_test/also_nope.txt /tmp/symlink_test/sub/bad_link2
#   ./find_broken_symlinks.sh /tmp/symlink_test
# should print exactly:
#   /tmp/symlink_test/bad_link
#   /tmp/symlink_test/sub/bad_link2
# (good_link should NOT appear -- its target actually exists.)
#
# HOW TO WORK THROUGH THIS
# -------------------------
# `find "$1" -type l` lists every symlink, full path, recursively.
# For each one, `[ -e "$link" ]` tests whether it resolves to
# something that exists -- crucially, `-e` FOLLOWS symlinks, so it's
# false for a symlink whose target is missing, which is exactly the
# broken case you want. (GNU find's `-xtype l` can do this in one
# step, but it's not portable to every find implementation, so the
# `-type l` + `[ ! -e ]` combination is the more portable route here.)
# Collect the ones that fail that test and sort the final output.

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

# TODO: replace this line with your implementation.
echo "not implemented" >&2
exit 1
