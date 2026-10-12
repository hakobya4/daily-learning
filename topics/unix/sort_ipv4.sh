#!/usr/bin/env bash
#
# Day 22, Task 6 -- Unix/shell: sort IPv4 addresses numerically.
#
# THE PROBLEM
# ------------
# stdin has one IPv4 address per line (dotted quad, e.g. 10.0.0.2).
# Print them sorted numerically octet by octet (so 10.0.0.2 comes before
# 10.0.0.10), removing exact duplicates.
#
#   input:  192.168.1.10 / 10.0.0.2 / 10.0.0.10 / 10.0.0.2
#   output: 10.0.0.2 / 10.0.0.10 / 192.168.1.10   (one per line)
#
# HOW TO WORK THROUGH THIS
# -------------------------
# sort -t. with four -k keys: -k1,1n -k2,2n -k3,3n -k4,4n, plus -u.
# (Careful: -u with several keys dedupes on the keys, which is fine here.)
#
# Check with:
#   printf '192.168.1.10\n10.0.0.2\n10.0.0.10\n10.0.0.2\n' | ./sort_ipv4.sh

sort -t. -k1,1n -k2,2n -k3,3n -k4,4n -u
