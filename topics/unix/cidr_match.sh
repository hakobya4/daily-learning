#!/usr/bin/env bash
#
# Day 63, Task 5 -- Unix/shell: longest-prefix-match IPv4 addresses against a CIDR table
# (what a router's forwarding table does), in plain bash + awk.
#
# THE PROBLEM
# ------------
# Usage: ./cidr_match.sh CIDR_FILE < ips.txt
#
# CIDR_FILE has one route per line: "<a.b.c.d>/<len>  <label>" separated by spaces/tabs.
# Everything from '#' to the end of a line is a comment; blank (or comment-only) lines
# are skipped. Example (save as cidrs.txt):
#
#   # office and cloud ranges
#   10.0.0.0/8        corp
#   10.20.0.0/16      corp-toronto
#   10.20.30.0/24     lab
#   192.168.1.0/24    home   # trailing comment
#   0.0.0.0/0         internet
#   10.20.30.128/25   lab-dmz
#   172.16.0.0/12     docker
#   10.20.0.0/16      duplicate-ignored
#
# For every line of stdin (trim surrounding whitespace; skip lines that are then empty)
# print ONE line: the IP, a TAB, then
#   - "<label> (<cidr as written>)" of the matching route with the LONGEST prefix
#     (if several routes with the same length match, the one listed FIRST wins -- that is
#     why "duplicate-ignored" never shows up);
#   - "-" if no route matches;
#   - "invalid" if the line is not a valid dotted-quad: exactly 4 decimal parts, each
#     0-255, no leading zeros ("01.2.3.4" is invalid, "0.0.0.0" is fine).
# Before reading any IPs, validate the whole CIDR_FILE. A route is invalid if the address
# is not a valid dotted-quad, the length is not an integer 0-32, the label is missing, or
# HOST BITS are set (10.1.2.0/8 is wrong -- it should be 10.0.0.0/8). On the first bad
# line print "line N: bad cidr" (N = physical line number in the file, counting blank and
# comment lines) -- or "line N: host bits set" for the host-bits case -- to stderr and
# exit 2 without printing anything to stdout. Wrong argument count or unreadable file:
# a usage line on stderr, exit 2.
#
# HINT: turn an address into one number v = ((a*256 + b)*256 + c)*256 + d. awk numbers
# are doubles, which hold 32-bit integers exactly, and you do NOT need bitwise operators
# (mawk has none): with d = 2^(32 - len), an IP is inside a route iff
# int(ip / d) == int(net / d), and host bits are set iff net % d != 0. Load the routes in
# a BEGIN block with `while ((getline line < file) > 0)`, then let the main rule handle
# stdin. Linear scan over the routes is fine.
#
# Check with (cidrs.txt as above):
#   printf '%s\n' 10.20.30.200 10.20.30.5 10.20.99.1 10.1.2.3 192.168.1.77 \
#     172.31.255.255 172.32.0.1 8.8.8.8 '  10.20.30.128  ' '' 256.1.1.1 10.1.2 \
#     01.2.3.4 abc 0.0.0.0 255.255.255.255 | ./cidr_match.sh cidrs.txt
# must print exactly (<TAB> = one tab character):
#   10.20.30.200<TAB>lab-dmz (10.20.30.128/25)
#   10.20.30.5<TAB>lab (10.20.30.0/24)
#   10.20.99.1<TAB>corp-toronto (10.20.0.0/16)
#   10.1.2.3<TAB>corp (10.0.0.0/8)
#   192.168.1.77<TAB>home (192.168.1.0/24)
#   172.31.255.255<TAB>docker (172.16.0.0/12)
#   172.32.0.1<TAB>internet (0.0.0.0/0)
#   8.8.8.8<TAB>internet (0.0.0.0/0)
#   10.20.30.128<TAB>lab-dmz (10.20.30.128/25)
#   256.1.1.1<TAB>invalid
#   10.1.2<TAB>invalid
#   01.2.3.4<TAB>invalid
#   abc<TAB>invalid
#   0.0.0.0<TAB>internet (0.0.0.0/0)
#   255.255.255.255<TAB>internet (0.0.0.0/0)
#   printf '10.0.0.0/8 x\n' > one.txt; echo 1.2.3.4 | ./cidr_match.sh one.txt
#                                         -> "1.2.3.4<TAB>-"
#   printf '10.0.0.0/8 a\n10.1.0.0/33 b\n' > bad1.txt; ./cidr_match.sh bad1.txt </dev/null
#                                         -> stderr "line 2: bad cidr", exit 2
#   printf '10.0.0.0/8 a\n\n10.1.2.0/8 b\n' > bad2.txt; ./cidr_match.sh bad2.txt </dev/null
#                                         -> stderr "line 3: host bits set", exit 2
#   printf '10.0.0.0/8\n' > bad3.txt; ./cidr_match.sh bad3.txt </dev/null
#                                         -> stderr "line 1: bad cidr" (no label), exit 2
#   ./cidr_match.sh                       -> usage on stderr, exit 2

set -u

usage() { echo "usage: $0 CIDR_FILE < ips.txt" >&2; exit 2; }

[ "$#" -eq 1 ] || usage
[ -f "$1" ] && [ -r "$1" ] || usage

exec awk -v file="$1" '
# dotted-quad -> number, or -1 if invalid
function ip2num(s,    p, n, i, v) {
    n = split(s, p, ".")
    if (n != 4) return -1
    v = 0
    for (i = 1; i <= 4; i++) {
        if (p[i] !~ /^(0|[1-9][0-9]?[0-9]?)$/) return -1
        if (p[i] + 0 > 255) return -1
        v = v * 256 + p[i]
    }
    # reject anything split() would hide (e.g. trailing dot is n==5 anyway)
    return v
}
function trim(s) { sub(/^[ \t\r]+/, "", s); sub(/[ \t\r]+$/, "", s); return s }
BEGIN {
    nr = 0; lineno = 0
    while ((getline line < file) > 0) {
        lineno++
        sub(/#.*/, "", line)
        line = trim(line)
        if (line == "") continue
        # first field = cidr, rest = label
        if (match(line, /[ \t]+/)) {
            cidr = substr(line, 1, RSTART - 1)
            label = trim(substr(line, RSTART + RLENGTH))
        } else {
            cidr = line; label = ""
        }
        if (label == "" || cidr !~ /^[0-9.]+\/(0|[1-9][0-9]?)$/) {
            print "line " lineno ": bad cidr" > "/dev/stderr"; exit 2
        }
        slash = index(cidr, "/")
        addr = substr(cidr, 1, slash - 1)
        len = substr(cidr, slash + 1) + 0
        net = ip2num(addr)
        if (net < 0 || len > 32) {
            print "line " lineno ": bad cidr" > "/dev/stderr"; exit 2
        }
        d = 2 ^ (32 - len)
        if (net % d != 0) {
            print "line " lineno ": host bits set" > "/dev/stderr"; exit 2
        }
        nr++
        R_net[nr] = net; R_div[nr] = d; R_len[nr] = len
        R_out[nr] = label " (" cidr ")"
    }
    close(file)
}
{
    ip = trim($0)
    if (ip == "") next
    v = ip2num(ip)
    if (v < 0) { print ip "\tinvalid"; next }
    best = 0; bestlen = -1
    for (i = 1; i <= nr; i++) {
        if (R_len[i] > bestlen && int(v / R_div[i]) == int(R_net[i] / R_div[i])) {
            best = i; bestlen = R_len[i]
        }
    }
    print ip "\t" (best ? R_out[best] : "-")
}
'
