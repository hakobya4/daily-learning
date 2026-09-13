#!/usr/bin/env bash
#
# Day 2, Task 3 -- Unix/shell: word frequency counter.
#
# THE PROBLEM
# ------------
# Given a text file (path passed as $1), print the top 5 most frequent
# words and their counts, one per line, most frequent first. Treat
# words case-insensitively and strip punctuation.
#
# This is a classic pipeline exercise: the goal is to solve it by
# CHAINING small Unix tools (tr, sort, uniq -c, sort, head) rather than
# writing a loop -- that pipeline-of-small-tools habit is the actual
# Unix skill being practiced here, not just "get the right answer."
#
# Useful building blocks (look up any you don't know):
#   tr 'A-Z' 'a-z'          -- lowercase
#   tr -cs 'a-z' '\n'       -- squeeze anything that's not a-z into newlines
#                              (this both splits into one-word-per-line
#                              AND strips punctuation in one step)
#   sort | uniq -c          -- count occurrences of each unique line
#   sort -rn                -- sort numerically, descending
#   head -n 5               -- take the top 5
#
# HOW TO WORK THROUGH THIS
# -------------------------
# Build the pipeline piece by piece in your terminal directly (not in
# this file) -- run each stage and look at the output before adding
# the next `|` stage. Once it works, paste the finished pipeline below.
#
# Test with: ./word_frequency.sh sample.txt
# (create sample.txt yourself with a few sentences, repeat some words)

if [ -z "$1" ]; then
    echo "Usage: $0 <textfile>" >&2
    exit 1
fi

# TODO: replace the line below with your real pipeline.
echo "TODO: not implemented yet"
