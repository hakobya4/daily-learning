#!/usr/bin/env bash
#
# Day 55, Task 5 -- Unix/shell: per-endpoint latency percentiles (nearest-rank).
#
# THE PROBLEM
# ------------
# Usage: ./latency_percentiles.sh FILE
# Each line of FILE is an access-log record of whitespace-separated fields:
#     METHOD PATH STATUS LATENCY_MS
# e.g.  GET /api/users 200 37
# For every distinct "METHOD PATH" pair, print one line:
#     METHOD PATH count=C p50=X p90=Y p99=Z max=M
# where the percentiles use the NEAREST-RANK method on that endpoint's latencies sorted
# ascending: the p-th percentile is the value at 1-based rank ceil(p/100 * C).
# Sort the output lines by p99 DESCENDING (slowest tail first), ties broken by
# "METHOD PATH" ascending.
# Lines that do not have exactly 4 fields, or whose STATUS is not a 3-digit number, or
# whose LATENCY_MS is not a non-negative integer, are skipped; print "skipped N" to STDERR
# at the end (always, even when N is 0).
# Exit 1 with a usage message on stderr if the argument count is wrong or FILE is not a
# readable regular file.
#
# HINT: one way is `sort -k1,1 -k2,2 -k4,4n` first so each endpoint's latencies arrive
# grouped and ascending, then a single awk pass that buffers one group at a time and emits
# its stats when the key changes (and in END). Integer ceil in awk:
#     r = int(p * c / 100); if (r * 100 < p * c) r++
# Finally pipe through  sort -t= ...  or  sort -k...  for the p99-descending order -- the
# p99 value is inside "p99=Z", so think about which field/separator to sort on (or emit the
# p99 as a hidden first column, sort, then strip it with cut).
#
# Check with:
#   printf '%s\n' 'GET /a 200 10' 'GET /a 200 20' 'GET /a 500 30' 'GET /a 200 40' \
#     'GET /a 200 50' 'POST /b 201 5' 'POST /b 201 500' 'GET /c 200 7' 'bad line' \
#     'GET /a 2x0 9' 'GET /c 200 -3' 'GET /c 200 99' > /tmp/d55.log
#   ./latency_percentiles.sh /tmp/d55.log
# Expected stdout:
#   POST /b count=2 p50=5 p90=500 p99=500 max=500
#   GET /c count=2 p50=7 p90=99 p99=99 max=99
#   GET /a count=5 p50=30 p90=50 p99=50 max=50
# Expected stderr:
#   skipped 3

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

skipfile=$(mktemp) || exit 1
trap 'rm -f "$skipfile"' EXIT

# 1) validate and keep "METHOD PATH LATENCY"; the skipped count goes to a temp file
#    so it can be printed AFTER the report.
# 2) group by endpoint with latencies ascending.
# 3) one pass emitting nearest-rank stats per group, with p99 as a hidden first column.
# 4) sort by p99 desc, then METHOD PATH asc, and strip the hidden column.
awk -v skipfile="$skipfile" '
    NF == 4 && $3 ~ /^[0-9][0-9][0-9]$/ && $4 ~ /^[0-9]+$/ { print $1, $2, $4; next }
    { skipped++ }
    END { print skipped + 0 > skipfile }
' "$1" |
LC_ALL=C sort -k1,1 -k2,2 -k3,3n |
awk '
    function rank(p, c,    r) { r = int(p * c / 100); if (r * 100 < p * c) r++; return r }
    function flush(    p50, p90, p99) {
        if (cnt == 0) return
        p50 = v[rank(50, cnt)]; p90 = v[rank(90, cnt)]; p99 = v[rank(99, cnt)]
        printf "%s %s count=%d p50=%s p90=%s p99=%s max=%s\n", p99, key, cnt, p50, p90, p99, v[cnt]
        cnt = 0
    }
    { k = $1 " " $2; if (k != key) { flush(); key = k } v[++cnt] = $3 }
    END { flush() }
' |
LC_ALL=C sort -k1,1nr -k2,2 -k3,3 |
cut -d' ' -f2-

echo "skipped $(cat "$skipfile")" >&2
