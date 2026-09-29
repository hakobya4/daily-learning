#!/usr/bin/env bash
#
# Day 9, Task 5 -- Unix/shell: top N client IPs from an access log.
#
# THE PROBLEM
# ------------
# $1 is a log file whose lines start with an IP address followed by a
# space and anything else (e.g. "10.0.0.1 GET /index 200"). $2 is N.
# Print the N most frequent IPs as "<count> <ip>", most frequent first;
# break ties by IP in ascending order.
#
# Example: given lines from 10.0.0.1 x3, 10.0.0.2 x1, 10.0.0.3 x3 and
# N=2, the output is:
#   3 10.0.0.1
#   3 10.0.0.3
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Think pipeline: extract field 1 (awk '{print $1}' or cut -d' ' -f1),
# sort, count with uniq -c, then sort by count descending with a
# secondary key, then head -n. Beware uniq -c pads counts with spaces.

if [ $# -ne 2 ]; then
    echo "Usage: $0 <logfile> <N>" >&2
    exit 1
fi

# TODO: replace this line (hint: awk | sort | uniq -c | sort | head)
echo "not implemented" >&2
exit 1
