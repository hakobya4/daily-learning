#!/usr/bin/env bash
#
# Day 56, Task 5 -- Unix/shell: sort version strings by Semantic Versioning precedence.
#
# THE PROBLEM
# ------------
# Usage: ./semver_sort.sh FILE
# Each line of FILE should be a SemVer 2.0 version, optionally prefixed with "v":
#     [v]MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
#   * MAJOR, MINOR, PATCH: non-negative integers with NO leading zeros ("0" ok, "01" not).
#   * PRERELEASE: one or more dot-separated identifiers of [0-9A-Za-z-]; an identifier
#     that is all digits must not have a leading zero; empty identifiers ("a..1") invalid.
#   * BUILD: one or more dot-separated identifiers of [0-9A-Za-z-]; IGNORED for ordering.
# Print the VALID lines exactly as they appeared, sorted ascending by SemVer precedence:
#   1. Compare MAJOR, MINOR, PATCH numerically.
#   2. A version WITH a prerelease is LOWER than the same version without one.
#   3. Prerelease identifiers are compared left to right: numeric ones numerically,
#      alphanumeric ones in ASCII order, and a numeric identifier is always LOWER than an
#      alphanumeric one. If all compared identifiers are equal, the SHORTER list is lower.
#   4. Lines of equal precedence (e.g. differing only in "v" or +BUILD) keep input order.
# Invalid lines are skipped; print "invalid N" to STDERR at the end (always, even N=0).
# Exit 1 with a usage message on stderr if the argument count is wrong or FILE is not a
# readable regular file.
#
# HINT: `sort -V` gets prerelease ordering WRONG (try it: it puts 1.0.0-alpha after
# 1.0.0) -- that's the point of the exercise. One approach: validate with a regex in awk,
# then emit a fixed-width SORT KEY per line, e.g. zero-padded major/minor/patch, a flag
# that is 0 for prerelease / 1 for release, then each prerelease identifier encoded so
# plain string comparison works (numeric -> "0" + zero-padded number, alnum -> "1" + text),
# plus the line number for stability; then `LC_ALL=C sort` on the key and `cut` it off.
# (Watch out: "beta" vs "beta.2" -- the shorter one must sort first; think about which
# separator character sorts lower than any identifier character in the C locale.)
#
# Check with:
#   printf '%s\n' '1.0.0' 'v1.0.0-alpha' '1.0.0-alpha.1' '1.0.0-alpha.beta' '1.0.0-beta' \
#     '1.0.0-beta.11' '1.0.0-beta.2' '1.0.0-rc.1' '2.0.0' '1.10.0' '1.2.0' 'not.a.version' \
#     '1.0' '01.2.3' '1.0.0+build.5' '1.0.0-alpha+exp' '0.9.9' '1.0.0-1' '1.0.0-alpha..1' \
#     > /tmp/d56.versions
#   ./semver_sort.sh /tmp/d56.versions
# Expected stdout:
#   0.9.9
#   1.0.0-1
#   v1.0.0-alpha
#   1.0.0-alpha+exp
#   1.0.0-alpha.1
#   1.0.0-alpha.beta
#   1.0.0-beta
#   1.0.0-beta.2
#   1.0.0-beta.11
#   1.0.0-rc.1
#   1.0.0
#   1.0.0+build.5
#   1.2.0
#   1.10.0
#   2.0.0
# Expected stderr:
#   invalid 4

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

# Validate each line in awk and emit "<sort key>\t<original line>"; the key is built
# so that a plain byte-wise (LC_ALL=C) string comparison gives SemVer precedence:
#   * numbers -> 2-digit length + digits (so longer numbers sort later, no overflow)
#   * flag "0" for a prerelease, "1" for a release
#   * prerelease ids: numeric -> "0"+num-key, alnum -> "1"+text, joined by \002 and
#     terminated by \001 (both lower than any identifier char, so a shorter list wins)
# A stable sort on the key keeps input order for equal precedence.
awk '
function numkey(n) { return sprintf("%02d", length(n)) n }
BEGIN { bad = 0 }
{
    line = $0
    v = line
    sub(/^v/, "", v)
    build = ""
    if (index(v, "+") > 0) {
        build = substr(v, index(v, "+") + 1)
        v = substr(v, 1, index(v, "+") - 1)
        if (build !~ /^[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*$/) { bad++; next }
    }
    pre = ""
    haspre = 0
    if (index(v, "-") > 0) {
        pre = substr(v, index(v, "-") + 1)
        v = substr(v, 1, index(v, "-") - 1)
        haspre = 1
        if (pre !~ /^[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*$/) { bad++; next }
    }
    if (v !~ /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$/) { bad++; next }
    split(v, c, ".")
    key = numkey(c[1]) "." numkey(c[2]) "." numkey(c[3]) "."
    if (haspre) {
        n = split(pre, ids, ".")
        pk = ""
        ok = 1
        for (i = 1; i <= n; i++) {
            id = ids[i]
            if (id ~ /^[0-9]+$/) {
                if (id ~ /^0[0-9]/) { ok = 0; break }
                enc = "0" numkey(id)
            } else {
                enc = "1" id
            }
            pk = pk (i > 1 ? "\002" : "") enc
        }
        if (!ok) { bad++; next }
        key = key "0" pk "\001"
    } else {
        key = key "1"
    }
    print key "\t" line
}
END { print "invalid " bad > "/dev/stderr" }
' "$1" | LC_ALL=C sort -s -t "$(printf '\t')" -k1,1 | cut -f2-
