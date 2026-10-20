#!/usr/bin/env bash
#
# Day 29, Task 6 -- Unix/shell: print palindromic lines.
#
# THE PROBLEM
# ------------
# Print every stdin line that reads the same forwards and backwards,
# IGNORING case and ignoring every non-alphanumeric character (spaces,
# punctuation). Lines that contain no alphanumeric characters are skipped.
# Keep the original line text and order.
#
# HOW TO WORK THROUGH THIS
# -------------------------
# For each line build a normalised copy: tolower($0) then gsub(/[^a-z0-9]/,
# "", s). Compare it with its reverse (build the reverse with a loop over
# substr, or use `rev` in a pipeline with paste). Skip when s == "".
#
# Check with:
#   printf 'A man, a plan, a canal: Panama\nhello\nRacecar\n!!!\nNo lemon, no melon\n' | ./palindromic_lines.sh
# Expected:
#   A man, a plan, a canal: Panama
#   Racecar
#   No lemon, no melon

awk '{
  s = tolower($0); gsub(/[^a-z0-9]/, "", s)
  if (s == "") next
  r = ""
  for (i = length(s); i >= 1; i--) r = r substr(s, i, 1)
  if (s == r) print $0
}'
