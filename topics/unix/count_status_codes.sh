#!/usr/bin/env bash
#
# Day 13, Task 4 -- Unix/shell: HTTP status code summary.
#
# THE PROBLEM
# ------------
# $1 is an access log in this format (space separated):
#   IP METHOD PATH STATUS BYTES
# Print one line per status CLASS (2xx, 3xx, 4xx, 5xx) that occurs, as
#   <class> <count> <total_bytes>
# sorted by class ascending, e.g.
#   2xx 3 1500
#   4xx 1 0
# Lines with fewer than 5 fields or a non-numeric status are ignored.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: skip bad lines, class = substr($4,1,1) "xx", accumulate count[c]++
# and bytes[c]+=$5 in END, pipe into sort.
#
# Check with:
#   printf '1.1.1.1 GET /a 200 500\n1.1.1.2 GET /b 404 0\n1.1.1.3 GET /c 200 1000\nbad line\n' | ./count_status_codes.sh /dev/stdin
#   -> "2xx 2 1500" then "4xx 1 0"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <logfile>" >&2
    exit 1
fi

awk '
    NF >= 5 && $4 ~ /^[0-9]+$/ && $5 ~ /^[0-9]+$/ {
        c = substr($4, 1, 1) "xx"
        count[c]++
        bytes[c] += $5
    }
    END { for (c in count) print c, count[c], bytes[c] }
' "$1" | LC_ALL=C sort
