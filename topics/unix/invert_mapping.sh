#!/usr/bin/env bash
#
# Day 18, Task 6 -- Unix/shell: invert a one-to-many mapping.
#
# THE PROBLEM
# ------------
# stdin lines look like  "key: v1,v2,v3". Print the inverted mapping
# "value: key1,key2" -- one line per distinct value, values in sorted
# order, and keys for each value in first-appearance (input) order.
#
#   input:  a: x,y / b: y,z
#   output: x: a / y: a,b / z: b
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk -F': ' then split($2, vs, ","); build out[v] = out[v] (out[v] ? "," : "") key;
# sort the value names at the end (pipe to sort).
#
# Check with:
#   printf 'a: x,y\nb: y,z\n' | ./invert_mapping.sh

awk -F': ' 'NF >= 2 {
    n = split($2, vs, ",")
    for (i = 1; i <= n; i++) {
        v = vs[i]
        gsub(/^[ \t]+|[ \t]+$/, "", v)
        if (v == "") continue
        out[v] = out[v] (out[v] != "" ? "," : "") $1
    }
}
END { for (v in out) print v ": " out[v] }' | sort
