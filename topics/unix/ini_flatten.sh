#!/usr/bin/env bash
#
# Day 54, Task 4 -- Unix/shell: flatten an INI file into section.key=value lines.
#
# THE PROBLEM
# ------------
# Usage: ./ini_flatten.sh FILE
# Read an INI-style file and print one line per key as  section.key=value
#   * A section header looks like  [name]  (optional spaces around it and inside the
#     brackets are trimmed: "  [ db ]  " is section "db").
#   * A key line looks like  key = value  -- split on the FIRST '=' only (values may contain
#     '='), trim leading/trailing spaces and tabs from both key and value. An empty value
#     is allowed ("key =" prints "section.key=").
#   * Keys that appear BEFORE any section header are printed WITHOUT a prefix: key=value.
#   * Blank (or whitespace-only) lines and comment lines whose first non-blank character
#     is ';' or '#' are ignored.
#   * Any other line (no '=' and not a header, or an empty key like "= x") is malformed:
#     print "line N: malformed" to stderr (N = 1-based line number in the file) and exit 2
#     immediately (lines already printed stay printed).
# Exit 1 (usage message on stderr) if the argument count is wrong or FILE is not a readable
# regular file.
#
# HINT: one awk program. Track the current section in a variable; use match()/sub()/gsub()
# to trim; index($0, "=") finds the first '=' so substr() can split key and value without
# relying on -F'=' (which would break values containing '='). Exit codes from awk propagate
# if you `exit 2` inside it and it is the last command.
#
# Check with:
#   printf 'debug = true\n\n; comment\n[ db ]\nhost=localhost\n  port =  5432 \n\n# x\n[app]\nurl = http://h/?a=1&b=2\nempty =\n' > /tmp/d54.ini
#   ./ini_flatten.sh /tmp/d54.ini
# Expected:
#   debug=true
#   db.host=localhost
#   db.port=5432
#   app.url=http://h/?a=1&b=2
#   app.empty=
#
#   printf '[s]\na=1\noops\nb=2\n' > /tmp/d54bad.ini
#   ./ini_flatten.sh /tmp/d54bad.ini; echo "exit=$?"
# Expected stdout:
#   s.a=1
#   exit=2
# Expected stderr:
#   line 3: malformed

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

awk '
function trim(s) {
    sub(/^[ \t]+/, "", s)
    sub(/[ \t\r]+$/, "", s)
    return s
}
{
    line = trim($0)
    if (line == "" || substr(line, 1, 1) == ";" || substr(line, 1, 1) == "#")
        next
    if (line ~ /^\[.*\]$/) {
        section = trim(substr(line, 2, length(line) - 2))
        next
    }
    eq = index(line, "=")
    if (eq == 0) {
        print "line " NR ": malformed" > "/dev/stderr"
        exit 2
    }
    key = trim(substr(line, 1, eq - 1))
    val = trim(substr(line, eq + 1))
    if (key == "") {
        print "line " NR ": malformed" > "/dev/stderr"
        exit 2
    }
    if (section == "")
        print key "=" val
    else
        print section "." key "=" val
}
' "$1"
