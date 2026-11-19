#!/usr/bin/env bash
#
# Day 59, Task 6 -- Unix/shell: CSV (with quoted fields) to an aligned Markdown table.
#
# THE PROBLEM
# ------------
# Usage: ./csv_to_markdown.sh [FILE]                  (reads stdin when FILE is omitted)
# Parse CSV the RFC 4180 way (no embedded newlines): fields are separated by ",";
# a field that STARTS with a double quote is quoted -- inside it "," is literal and ""
# stands for one literal ". A quote in the middle of an unquoted field is just a
# character. A trailing "\r" (Windows line ending) is stripped from each line.
# Line 1 is the header and fixes the column count C. A data row with FEWER than C fields
# is padded with empty cells; MORE than C fields -> "line N: too many fields" on stderr,
# exit 1, nothing on stdout. A quote that is never closed -> "line N: unterminated
# quote", exit 1. Empty input -> "no header" on stderr, exit 1.
# Output a GitHub Markdown table:
#   | h1  | h2 |          every cell padded with spaces to its column's width,
#   | --- | -: |          width = longest cell text in that column (header included),
#   | x   |  5 |          but at least 3
# * Every "|" inside a cell is written as "\|" (the backslash counts toward width).
# * A column is NUMERIC if it has at least one non-empty data cell and every non-empty
#   data cell matches ^-?[0-9]+(\.[0-9]+)?$ . Numeric columns are right-aligned (header
#   included) and their separator is width-1 dashes followed by ":"; other columns are
#   left-aligned with a separator of width dashes.
# Exit 2 with a usage message for extra arguments or an unreadable FILE.
#
# HINT: gawk's FPAT cannot cope with "" escapes AND empty fields cleanly, so write a
# small character-by-character parse(line, out) function in awk with an in_quotes flag.
# Store all cells in cell[row, col] and track width[col] / numeric flags while reading;
# print everything in END with sprintf("%-" w "s") or sprintf("%" w "s"). Remember an
# `exit 1` in a main rule still runs END -- guard it with a flag.
#
# Check with:
#   printf '%s\n' 'name,qty,price,note' 'apple,3,1.25,"red, crisp"' 'kiwi,12,0.5,' \
#     '"Banana ""XL""",7,-2,a|b' 'fig,,10' > /tmp/t.csv
#   ./csv_to_markdown.sh /tmp/t.csv; echo "exit=$?"
# Expected:
#   | name        | qty | price | note       |
#   | ----------- | --: | ----: | ---------- |
#   | apple       |   3 |  1.25 | red, crisp |
#   | kiwi        |  12 |   0.5 |            |
#   | Banana "XL" |   7 |    -2 | a\|b       |
#   | fig         |     |    10 |            |
#   exit=0
#   printf 'a,b\n1,2,3\n' | ./csv_to_markdown.sh   -> stderr "line 2: too many fields", exit 1
#   printf 'a,b\n"x,1\n'  | ./csv_to_markdown.sh   -> stderr "line 2: unterminated quote", exit 1
#   printf 'id\n'         | ./csv_to_markdown.sh   -> "| id  |" and "| --- |", exit 0

usage() {
    echo "usage: $0 [FILE]" >&2
    exit 2
}

[ $# -le 1 ] || usage
if [ $# -eq 1 ]; then
    { [ -f "$1" ] && [ -r "$1" ]; } || usage
    exec < "$1"
fi

awk '
    # Split one CSV line into out[1..n]; returns n, or -1 on an unterminated quote.
    function parse(line, out,    n, i, c, len, field, inq, quoted) {
        n = 0; field = ""; inq = 0; quoted = 0
        len = length(line)
        for (i = 1; i <= len; i++) {
            c = substr(line, i, 1)
            if (inq) {
                if (c == "\"") {
                    if (substr(line, i + 1, 1) == "\"") { field = field "\""; i++ }
                    else inq = 0
                } else field = field c
            } else if (c == ",") {
                out[++n] = field; field = ""; quoted = 0
            } else if (c == "\"" && field == "" && !quoted) {
                inq = 1; quoted = 1
            } else field = field c
        }
        if (inq) return -1
        out[++n] = field
        return n
    }
    {
        sub(/\r$/, "")
        split("", f)
        n = parse($0, f)
        if (n < 0) { print "line " NR ": unterminated quote" > "/dev/stderr"; failed = 1; exit 1 }
        if (NR == 1) {
            C = n
            for (c = 1; c <= C; c++) { width[c] = 3; numeric[c] = 1; nonempty[c] = 0 }
        } else if (n > C) {
            print "line " NR ": too many fields" > "/dev/stderr"; failed = 1; exit 1
        }
        for (c = 1; c <= C; c++) {
            v = (c <= n) ? f[c] : ""
            if (NR > 1 && v != "") {
                nonempty[c] = 1
                if (v !~ /^-?[0-9]+(\.[0-9]+)?$/) numeric[c] = 0
            }
            gsub(/\|/, "\\|", v)
            cell[NR, c] = v
            if (length(v) > width[c]) width[c] = length(v)
        }
        rows = NR
    }
    function emit(r,    c, line, fmt) {
        line = "|"
        for (c = 1; c <= C; c++) {
            fmt = (numeric[c] && nonempty[c]) ? "%" width[c] "s" : "%-" width[c] "s"
            line = line " " sprintf(fmt, cell[r, c]) " |"
        }
        print line
    }
    END {
        if (failed) exit 1
        if (rows == 0) { print "no header" > "/dev/stderr"; exit 1 }
        emit(1)
        line = "|"
        for (c = 1; c <= C; c++) {
            dashes = ""
            for (k = 0; k < width[c]; k++) dashes = dashes "-"
            if (numeric[c] && nonempty[c]) dashes = substr(dashes, 2) ":"
            line = line " " dashes " |"
        }
        print line
        for (r = 2; r <= rows; r++) emit(r)
    }
'
