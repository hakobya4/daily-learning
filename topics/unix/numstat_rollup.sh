#!/usr/bin/env bash
#
# Day 60, Task 6 -- Unix/shell: per-author churn from `git log --numstat` output.
#
# THE PROBLEM
# ------------
# Usage: ./numstat_rollup.sh [-n TOP] [FILE]        (reads stdin when FILE is omitted)
# The input is what `git log --numstat --format='@@ %an'` prints: a header line
#   @@ AUTHOR NAME            (the name may contain spaces)
# for every commit, followed by zero or more numstat lines
#   ADDED<TAB>REMOVED<TAB>PATH
# where ADDED/REMOVED are integers, or both "-" for a binary file. Blank lines are
# ignored. A numstat line that appears before the first header prints
# "line N: outside a commit" to STDERR; any other malformed line (not a header, not 3
# TAB-separated fields, or counts that are not integers / not both "-") prints
# "line N: malformed" to STDERR. Both are skipped; neither changes the exit status.
#
# For every author print one line:
#   AUTHOR: commits=C files=F added=A removed=R binary=B
# where C = number of headers for that author (commits with no numstat lines count too),
# F = DISTINCT paths that author touched (text or binary), A / R = summed line counts,
# B = number of binary numstat lines. Sort by A + R descending, then by AUTHOR
# ascending (plain byte order, LC_ALL=C). With -n TOP print only the first TOP authors.
# Then always print (over ALL authors, not just the shown ones):
#   TOTAL authors=X commits=C added=A removed=R
# Exit 2 with a usage line on stderr if TOP is not a positive integer, there are extra
# arguments, or FILE is not a readable regular file.
#
# HINT: awk -F'\t' with arrays keyed by author: commits[a]++, add[a] += $1, and
# seen[a SUBSEP $3] for distinct files (count a path the first time it is seen for that
# author). Print "A+R<TAB>AUTHOR<TAB>rest" in END, then `LC_ALL=C sort -t "<TAB>"
# -k1,1nr -k2,2`, `head -n TOP` if asked, and `cut -f2-` + a final awk/sed to format;
# compute the TOTAL line in the first awk and pass it out on a line that sorts last
# (or write it to a temp file).
#
# Check with:
#   printf '@@ Ann Lee\n3\t1\tsrc/a.py\n10\t0\tREADME.md\n\n@@ Bob\n-\t-\tlogo.png\n2\t2\tsrc/a.py\n' > /tmp/n.txt
#   printf '@@ Ann Lee\n1\t4\tsrc/a.py\n@@ Cy\n@@ Bob\n5\tx\tbad.txt\njunk line\n' >> /tmp/n.txt
#   printf '@@ Dee\n6\t0\tdocs/x.md\n' >> /tmp/n.txt
#   sed -i '1i 7\t7\torphan.txt' /tmp/n.txt
#   ./numstat_rollup.sh /tmp/n.txt; echo "exit=$?"
# Expected stdout:
#   Ann Lee: commits=2 files=2 added=14 removed=5 binary=0
#   Dee: commits=1 files=1 added=6 removed=0 binary=0
#   Bob: commits=2 files=2 added=2 removed=2 binary=1
#   Cy: commits=1 files=0 added=0 removed=0 binary=0
#   TOTAL authors=4 commits=6 added=22 removed=7
#   exit=0
# Expected stderr:
#   line 1: outside a commit
#   line 13: malformed
#   line 14: malformed
#   ./numstat_rollup.sh -n 2 /tmp/n.txt   -> the Ann Lee and Dee lines, then the same TOTAL
#   ./numstat_rollup.sh -n 0 /tmp/n.txt   -> usage on stderr, exit 2
# Real use: git log --numstat --format='@@ %an' | ./numstat_rollup.sh -n 5

echo "not implemented" >&2
# TODO: replace this line with your implementation
exit 1
