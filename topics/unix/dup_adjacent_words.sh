#!/usr/bin/env bash
#
# Day 33, Task 7 -- Unix/shell: report immediately repeated words.
#
# THE PROBLEM
# ------------
# stdin is lines of text. For every place where a word is immediately
# followed by the same word (case-insensitive), print "<line-number>: <word>"
# with the word in lower case. A word repeated three times in a row
# (the the the) is two repeats, so it prints twice. Words are separated by
# whitespace; line numbers start at 1; lines without repeats print nothing.
#
# Input:
#   this is is a test
#   no dups here
#   The the THE end
# Output:
#   1: is
#   3: the
#   3: the
#
# HINT: awk, looping i from 2..NF and comparing tolower($i) to tolower($(i-1)).
#
# Check with:
#   printf 'this is is a test\nno dups here\nThe the THE end\n' | ./dup_adjacent_words.sh
# Expected:
#   1: is
#   3: the
#   3: the

# TODO: replace this line
exit 1
