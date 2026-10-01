#!/usr/bin/env bash
#
# Day 10, Task 5 -- Unix/shell: join two CSV files on a key.
#
# THE PROBLEM
# ------------
# $1 = users.csv   lines: id,name          (e.g. "1,Ana")
# $2 = orders.csv  lines: user_id,amount   (e.g. "1,30")
# No header lines. Print "name,total" for every user that has at least
# one order, where total is the sum of that user's amounts. Sort output
# by name ascending. Users without orders are omitted; orders whose
# user_id is unknown are ignored.
#
# Example: users 1,Ana / 2,Bo ; orders 1,30 / 1,20 / 2,5 / 9,99
#   -> Ana,50
#      Bo,5
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Either the `join` command (inputs must be sorted on the key!) or an
# awk two-file idiom: while NR==FNR read users into an array, then sum
# orders by user; print in END, piped to sort.

if [ $# -ne 2 ]; then
    echo "Usage: $0 <users.csv> <orders.csv>" >&2
    exit 1
fi

awk -F, '
NR == FNR { name[$1] = $2; next }
($1 in name) { total[$1] += $2 }
END { for (id in total) print name[id] "," total[id] }
' "$1" "$2" | sort
