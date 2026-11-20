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

usage() {
    echo "usage: $(basename "$0") [-n TOP] [FILE]   (TOP must be a positive integer)" >&2
    exit 2
}

top=0
while getopts ":n:" opt; do
    case "$opt" in
        n) case "$OPTARG" in
               ''|*[!0-9]*) usage ;;
           esac
           [ "$((10#$OPTARG))" -gt 0 ] || usage
           top=$((10#$OPTARG)) ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))
[ $# -le 1 ] || usage
if [ $# -eq 1 ]; then
    { [ -f "$1" ] && [ -r "$1" ]; } || usage
    input="$1"
else
    input="-"
fi

# Stage 1: aggregate. Author rows are "0<TAB>churn<TAB>author<TAB>formatted line";
# the TOTAL row starts with "1" so it always sorts after every author.
awk -F'\t' '
function isint(s) { return s ~ /^[0-9]+$/ }
{
    sub(/\r$/, "")
    if ($0 == "") next
    if (substr($0, 1, 3) == "@@ ") {
        cur = substr($0, 4)
        if (!(cur in commits)) order[++na] = cur
        commits[cur]++
        ncommits++
        next
    }
    ok = (NF == 3 && $3 != "" && ((isint($1) && isint($2)) || ($1 == "-" && $2 == "-")))
    if (!ok) { printf "line %d: malformed\n", NR > "/dev/stderr"; next }
    if (cur == "" && !(cur in commits)) {
        printf "line %d: outside a commit\n", NR > "/dev/stderr"; next
    }
    if ($1 == "-") binary[cur]++
    else { added[cur] += $1; removed[cur] += $2; tadd += $1; trem += $2 }
    if (!((cur, $3) in seen)) { seen[cur, $3] = 1; files[cur]++ }
}
END {
    for (k = 1; k <= na; k++) {
        a = order[k]
        printf "0\t%d\t%s\t%s: commits=%d files=%d added=%d removed=%d binary=%d\n",
            added[a] + removed[a], a, a, commits[a], files[a] + 0,
            added[a] + 0, removed[a] + 0, binary[a] + 0
    }
    printf "1\t0\t\tTOTAL authors=%d commits=%d added=%d removed=%d\n",
        na, ncommits + 0, tadd + 0, trem + 0
}' "$input" |
LC_ALL=C sort -t "$(printf '\t')" -k1,1n -k2,2nr -k3,3 |
awk -F'\t' -v top="$top" '
$1 == "1" { print $4; next }
top == 0 || ++shown <= top { print $4 }'
