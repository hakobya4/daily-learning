#!/usr/bin/env bash
#
# Day 18, Task 5 -- Unix/shell: sum values per hour.
#
# THE PROBLEM
# ------------
# stdin lines look like:  2026-10-01 09:15 5
#                          (date, HH:MM, integer value)
# Print one line per distinct (date, hour): "2026-10-01 09 <sum>", sorted
# by date then hour. Skip blank lines.
#
#   input:  2026-10-01 09:15 5 / 2026-10-01 09:50 7 / 2026-10-01 10:01 1
#   output: 2026-10-01 09 12 / 2026-10-01 10 1
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: split($2, t, ":"); accumulate sum[$1 " " t[1]] += $3; then pipe
# the END output through sort.
#
# Check with:
#   printf '2026-10-01 09:15 5\n2026-10-01 09:50 7\n2026-10-01 10:01 1\n' | ./sum_by_hour.sh

awk 'NF >= 3 { split($2, t, ":"); sum[$1 " " t[1]] += $3 }
     END { for (k in sum) print k, sum[k] }' | sort
