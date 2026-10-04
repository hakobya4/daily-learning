#!/usr/bin/env bash
#
# Day 14, Task 4 -- Unix/shell: human-readable byte counts.
#
# THE PROBLEM
# ------------
# Read one non-negative integer (a byte count) per line from stdin and
# print each in 1024-based units with ONE decimal, except plain bytes:
#
#   0        -> 0B
#   999      -> 999B
#   1024     -> 1.0K
#   1536     -> 1.5K
#   1048576  -> 1.0M
#   5368709120 -> 5.0G
#
# Units are B, K, M, G, T (stop at T). Skip blank lines.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: loop while v >= 1024 and unit index < 4, dividing by 1024;
# printf "%.1f%s\n" for anything above B, "%dB" for bytes.
#
# Check with:
#   printf '0\n1536\n1048576\n' | ./human_size.sh   -> 0B / 1.5K / 1.0M

# TODO: replace this line with your awk program (read stdin, print results).
exit 1
