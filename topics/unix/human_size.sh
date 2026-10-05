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

awk '
NF == 0 { next }
{
    v = $1 + 0
    if (v < 1024) { printf "%dB\n", v; next }
    split("B K M G T", u, " ")
    i = 1
    while (v >= 1024 && i < 5) { v /= 1024; i++ }
    printf "%.1f%s\n", v, u[i]
}'
