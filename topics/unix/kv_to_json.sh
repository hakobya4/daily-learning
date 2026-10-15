#!/usr/bin/env bash
#
# Day 24, Task 6 -- Unix/shell: key=value lines to a JSON object.
#
# THE PROBLEM
# ------------
# stdin has lines of the form key=value (split on the FIRST '='; the value
# may itself contain '='). Skip blank lines and lines starting with '#'.
# Print ONE line of JSON: an object with the keys in input order and every
# value as a JSON string. Escape backslash and double quote inside values
# (\\ and \"). If a key repeats, the last value wins but the key keeps its
# first position. No input pairs -> print {}.
#
#   input:  name=Ann / # c / path=C:\tmp / q=say "hi" / name=Bob
#   output: {"name":"Bob","path":"C:\\tmp","q":"say \"hi\""}
#
# HOW TO WORK THROUGH THIS
# -------------------------
# awk: idx = index($0, "="); key = substr($0, 1, idx-1); val = substr($0, idx+1);
# gsub(/\\/, "\\\\", val) then gsub(/"/, "\\\"", val). Keep keys in an
# order[] array the first time you see them and values in vals[key].
#
# Check with:
#   printf 'name=Ann\n# c\npath=C:\\tmp\nq=say "hi"\nname=Bob\n' | ./kv_to_json.sh

awk '
/^[[:space:]]*$/ { next }
/^#/ { next }
{
  idx = index($0, "=")
  if (idx == 0) next
  key = substr($0, 1, idx - 1)
  val = substr($0, idx + 1)
  if (!(key in vals)) order[++n] = key
  vals[key] = val
}
function esc(s) {
  gsub(/\\/, "\\\\", s)
  gsub(/"/, "\\\"", s)
  return s
}
END {
  out = "{"
  for (i = 1; i <= n; i++) {
    if (i > 1) out = out ","
    out = out "\"" esc(order[i]) "\":\"" esc(vals[order[i]]) "\""
  }
  print out "}"
}'
