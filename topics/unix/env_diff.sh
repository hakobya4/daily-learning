#!/usr/bin/env bash
#
# Day 58, Task 6 -- Unix/shell: semantic diff of two .env files, with secret masking.
#
# THE PROBLEM
# ------------
# Usage: ./env_diff.sh OLD NEW
# OLD and NEW are .env-style files. Per line:
#   * blank lines (only whitespace) and lines whose first non-blank char is "#" are
#     ignored;
#   * an optional leading "export " is allowed ("export KEY=value");
#   * otherwise the line must be KEY=VALUE where KEY matches ^[A-Za-z_][A-Za-z0-9_]*$
#     (no spaces around KEY or "="). VALUE is EVERYTHING after the FIRST "=" (it may
#     contain "=" and spaces, and may be empty). If VALUE is wrapped in a matching pair
#     of double quotes or single quotes, strip that one pair;
#   * any other line is invalid: print "FILE:LINENO: invalid line" to STDERR and ignore
#     it (keep going);
#   * if a KEY appears several times in one file, the LAST occurrence wins.
# Compare the two key->value maps and print, sorted by KEY (LC_ALL=C order):
#   + KEY=NEWVALUE          key only in NEW
#   - KEY=OLDVALUE          key only in OLD
#   ~ KEY: OLD -> NEW       key in both, value changed
# Unchanged keys print nothing. If the KEY contains SECRET, PASSWORD, TOKEN or KEY as a
# substring (case-insensitive, so API_KEY and db_password count) print "***" instead
# of every value of that key (a changed secret prints "~ API_KEY: *** -> ***").
# Exit status (like diff): 0 if no differences, 1 if differences, 2 with a usage
# message if the argument count is wrong or either file is not a readable regular file.
#
# HINT: one awk program reading both files. Tell them apart by ARGIND-free logic that
# survives an EMPTY first file (the classic FNR == NR trick breaks then): e.g. count
# file switches in a rule on FNR == 1 and also check FILENAME == ARGV[1] (OLD and NEW
# may even be the same path). Strip "export " with sub(/^export /, ""), find the first
# "=" with index(line, "="), check the key with a regex, then store old[key] /
# new[key]. In END walk the union of keys; print "KEY<TAB>line" into
# `LC_ALL=C sort -t "<TAB>" -k1,1 | cut -f2-` (sorting the whole line would group by
# the +/-/~ sign) and set the exit code with exit(changed ? 1 : 0) -- remember a
# pipeline's exit status is the LAST command's, so capture awk's status (PIPESTATUS,
# or run sort from inside awk and close() it).
#
# Check with:
#   printf '%s\n' '# old' 'APP_NAME=shop' 'PORT=8080' 'DB_PASSWORD=hunter2' \
#     'export DEBUG=true' 'URL="http://x/?a=1"' 'bad line' 'PORT=8081' 'GONE=1' > /tmp/old.env
#   printf '%s\n' 'APP_NAME=shop' 'PORT=9090' "DB_PASSWORD='s3cret'" 'DEBUG=true' \
#     'URL=http://x/?a=1&b=2' '' '  # comment' 'NEW_FLAG=' 'api_key=abc' '1BAD=x' > /tmp/new.env
#   ./env_diff.sh /tmp/old.env /tmp/new.env; echo "exit=$?"
# Expected stdout:
#   ~ DB_PASSWORD: *** -> ***
#   - GONE=1
#   + NEW_FLAG=
#   ~ PORT: 8081 -> 9090
#   ~ URL: http://x/?a=1 -> http://x/?a=1&b=2
#   + api_key=***
#   exit=1
# Expected stderr:
#   /tmp/old.env:7: invalid line
#   /tmp/new.env:10: invalid line
#   ./env_diff.sh /tmp/old.env /tmp/old.env  -> no stdout, exit 0

usage() {
    echo "usage: $0 OLD NEW   (both must be readable regular files)" >&2
    exit 2
}

[ "$#" -eq 2 ] || usage
for f in "$1" "$2"; do
    [ -f "$f" ] && [ -r "$f" ] || usage
done

# Everything happens in BEGIN with getline, so an EMPTY old file (or OLD == NEW) is
# handled correctly -- no FNR == NR trick needed.
awk -v oldf="$1" -v newf="$2" '
function load(file, map,    line, lineno, eq, key, val) {
    lineno = 0
    while ((getline line < file) > 0) {
        lineno++
        if (line ~ /^[ \t]*$/ || line ~ /^[ \t]*#/) continue
        sub(/^export /, "", line)
        eq = index(line, "=")
        key = (eq > 0) ? substr(line, 1, eq - 1) : ""
        if (eq == 0 || key !~ /^[A-Za-z_][A-Za-z0-9_]*$/) {
            printf "%s:%d: invalid line\n", file, lineno > "/dev/stderr"
            continue
        }
        val = substr(line, eq + 1)
        if (length(val) >= 2 && (val ~ /^".*"$/ || val ~ /^\047.*\047$/))
            val = substr(val, 2, length(val) - 2)
        map[key] = val            # last occurrence wins
    }
    close(file)
}
function secret(key) { return toupper(key) ~ /SECRET|PASSWORD|TOKEN|KEY/ }
function show(key, val) { return secret(key) ? "***" : val }
BEGIN {
    load(oldf, old)
    load(newf, new)
    cmd = "LC_ALL=C sort -t \"\t\" -k1,1 | cut -f2-"
    changed = 0
    for (k in old) all[k] = 1
    for (k in new) all[k] = 1
    for (k in all) {
        if (!(k in old))
            line = "+ " k "=" show(k, new[k])
        else if (!(k in new))
            line = "- " k "=" show(k, old[k])
        else if (old[k] != new[k])
            line = "~ " k ": " show(k, old[k]) " -> " show(k, new[k])
        else
            continue
        changed = 1
        print k "\t" line | cmd
    }
    close(cmd)
    exit(changed ? 1 : 0)
}'
