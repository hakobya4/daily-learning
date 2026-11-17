#!/usr/bin/env bash
#
# Day 57, Task 6 -- Unix/shell: find clients that burst above a rate limit (sliding window).
#
# THE PROBLEM
# ------------
# Usage: ./rate_limit_offenders.sh N W FILE
# FILE is a request log, one request per line: "EPOCH_SECONDS IP", sorted by time
# ascending (ties possible). A valid line has exactly 2 fields, EPOCH is all digits and
# IP is four dot-separated groups of digits (no range check needed). Other lines are
# skipped and counted.
# For every IP compute the MAXIMUM number of its requests that fall inside any
# half-open window [t, t + W) where t is one of that IP's request times, and the
# EARLIEST such t that achieves this maximum.
# Print "IP MAX WINDOW_START" for every IP whose MAX >= N, sorted by MAX descending,
# then IP ascending (plain string order). Finally print "skipped K" to STDERR (always).
# Exit 1 with a usage message on stderr if the argument count is wrong, N or W is not a
# positive integer (no leading zeros), or FILE is not a readable regular file.
#
# HINT: in awk, store each IP's times in an array keyed by (ip, index) as you read
# (they arrive sorted), then in END run a two-pointer scan per IP: advance `lo` while
# t[hi] - t[lo] >= W; the window size is hi - lo + 1. Only replace the best on a
# STRICTLY larger count so the earliest start wins. Sort the output with
# `sort -k2,2nr -k1,1`. Validate N and W with [[ $x =~ ^[1-9][0-9]*$ ]].
#
# Check with:
#   printf '%s\n' '1000 10.0.0.1' '1001 10.0.0.2' '1002 10.0.0.1' '1005 10.0.0.1' \
#     '1009 10.0.0.1' '1010 10.0.0.1' '1011 10.0.0.3' 'garbage line here' \
#     '1012 10.0.0.2' '1013 10.0.0.1' '1014 10.0.0.2' '1020 10.0.0.3' '1021 10.0.0.3' \
#     '1022 10.0.0.3' '1024 999.x.0.1' '1025 10.0.0.3' '1030 10.0.0.2' '1031 10.0.0.2' \
#     '1032 10.0.0.2' > /tmp/d57.log
#   ./rate_limit_offenders.sh 3 10 /tmp/d57.log
# Expected stdout:
#   10.0.0.1 4 1000
#   10.0.0.3 4 1020
#   10.0.0.2 3 1030
# Expected stderr:
#   skipped 2
#   ./rate_limit_offenders.sh 0 10 /tmp/d57.log   -> usage message, exit 1

if [ "$#" -ne 3 ] || [ ! -f "$3" ] || [ ! -r "$3" ]; then
    echo "usage: $0 N W FILE" >&2
    exit 1
fi

N=$1
W=$2
if ! [[ $N =~ ^[1-9][0-9]*$ ]] || ! [[ $W =~ ^[1-9][0-9]*$ ]]; then
    echo "usage: $0 N W FILE (N and W must be positive integers)" >&2
    exit 1
fi

awk -v N="$N" -v W="$W" '
NF == 2 && $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ {
    ip = $2
    if (!(ip in cnt)) ips[++nips] = ip
    t[ip, ++cnt[ip]] = $1 + 0
    next
}
{ skipped++ }
END {
    for (k = 1; k <= nips; k++) {
        ip = ips[k]
        n = cnt[ip]
        best = 0; best_t = ""
        hi = 1
        # For each start time t[lo], count requests in [t[lo], t[lo] + W).
        for (lo = 1; lo <= n; lo++) {
            if (hi < lo) hi = lo
            while (hi + 1 <= n && t[ip, hi + 1] - t[ip, lo] < W) hi++
            size = hi - lo + 1
            if (size > best) { best = size; best_t = t[ip, lo] }
        }
        if (best >= N) print ip, best, best_t
    }
    printf "skipped %d\n", skipped + 0 > "/dev/stderr"
}
' "$3" | LC_ALL=C sort -k2,2nr -k1,1
