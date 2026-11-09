#!/usr/bin/env bash
#
# Day 48, Task 5 -- Unix/shell: group anagrams from a word list.
#
# THE PROBLEM
# ------------
# Usage: ./anagram_lines.sh FILE
# FILE has one word per line (lowercase letters). Print every group of two or more
# words that are anagrams of each other, one group per line: the words sorted
# alphabetically, separated by single spaces, duplicates of the same word counted once.
# Print the groups sorted by their first word. Words with no anagram partner are
# not printed. Exit 1 on bad usage or an unreadable FILE.
#
# HINT: build a key = the word's letters sorted (split into chars, sort, join), then
# group by key in awk (or sort | uniq) and sort the output.
#
# Check with:
#   printf 'listen\nsilent\nenlist\ngoogle\ngogole\ncat\nact\ntac\ndog\n' > /tmp/d48b
#   ./anagram_lines.sh /tmp/d48b
# Expected:
#   act cat tac
#   enlist listen silent
#   gogole google

if [ $# -ne 1 ] || [ ! -r "$1" ] || [ -d "$1" ]; then
  echo "usage: $0 FILE" >&2
  exit 1
fi

awk 'NF {
  n = split($1, c, "")
  for (i = 2; i <= n; i++) { v = c[i]; j = i - 1; while (j >= 1 && c[j] > v) { c[j+1] = c[j]; j-- } c[j+1] = v }
  key = ""; for (i = 1; i <= n; i++) key = key c[i]
  if (!(($1 SUBSEP key) in seen)) { seen[$1, key] = 1; words[key] = words[key] " " $1; cnt[key]++ }
}
END { for (k in cnt) if (cnt[k] > 1) print words[k] }' "$1" |
while read -r line; do
  printf '%s\n' "$(printf '%s\n' $line | LC_ALL=C sort | paste -sd' ' -)"
done | LC_ALL=C sort
