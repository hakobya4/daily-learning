#!/usr/bin/env bash
#
# Day 13, Task 5 -- Unix/shell: keep the first row per key.
#
# THE PROBLEM
# ------------
# $1 is a CSV file with a header line; $2 is a 1-based column number.
# Print the header, then only the FIRST row seen for each distinct value
# in column $2, keeping the original order of those rows. Assume no
# quoted commas.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk -F, 'NR==1 {print; next} !seen[$col]++' with -v col="$2".
#
# Check with:
#   printf 'id,name\n1,ann\n2,bob\n3,ann\n' | ./uniq_by_column.sh /dev/stdin 2
#   -> id,name / 1,ann / 2,bob

if [ $# -ne 2 ]; then
    echo "Usage: $0 <csv> <column>" >&2
    exit 1
fi

# TODO: replace this line
exit 1
