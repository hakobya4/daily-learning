#!/usr/bin/env bash
#
# Day 39, Task 5 -- Unix/shell: greedy word wrap.
#
# THE PROBLEM
# ------------
# Usage: ./fold_words.sh WIDTH   (text on stdin)
# Split all input into words (any whitespace, newlines included, separates
# words) and re-flow them into lines of at most WIDTH characters, joining
# words with single spaces, breaking only between words. A word longer than
# WIDTH goes on a line by itself, unbroken.
#
# HINT: awk with a current-line variable; if length(line)+1+length(word)
# exceeds the width, print the line and start a new one.
#
# Check with:
#   printf 'the quick brown fox jumps over\n' | ./fold_words.sh 10
# Expected:
#   the quick
#   brown fox
#   jumps over
#
#   printf 'a  b\nc extraordinarily d\n' | ./fold_words.sh 5
# Expected:
#   a b c
#   extraordinarily
#   d

awk -v w="$1" '
  {
    for (i = 1; i <= NF; i++) {
      if (line == "") line = $i
      else if (length(line) + 1 + length($i) <= w) line = line " " $i
      else { print line; line = $i }
    }
  }
  END { if (line != "") print line }'
