#!/usr/bin/env bash
#
# Day 63, Task 6 -- Unix/shell: a safe `envsubst`-like template renderer with defaults,
# `$$` escapes and strict errors -- WITHOUT eval, envsubst or sed-replacement hazards.
#
# THE PROBLEM
# ------------
# Usage: ./template_render.sh VARS_FILE < template.txt
#
# VARS_FILE: one KEY=VALUE per line. KEY matches [A-Za-z_][A-Za-z0-9_]*; VALUE is
# EVERYTHING after the FIRST '=' (it may contain '=', spaces, '&', '\', even '${...}',
# all taken literally; an empty VALUE is allowed). Lines that are blank or whose first
# non-blank character is '#' are skipped. Any other line without a valid KEY= prefix:
# "vars line N: bad assignment" on stderr, exit 2. Do NOT read the real environment --
# only VARS_FILE.
#
# Template rules, applied left to right in one pass on each line:
#   ${NAME}            -> the value of NAME; if NAME is not defined in VARS_FILE
#                         -> error "line N: undefined variable NAME"
#   ${NAME:-default}   -> the value of NAME if it is defined AND non-empty, else the
#                         literal text "default" (everything up to the closing '}')
#   $$                 -> a single literal '$' (so "$${PORT}" renders as "${PORT}")
#   any other '$'      -> itself ("$5", a lone "$ " are left alone)
#   "${" with no closing '}' on the same line -> error "line N: unterminated ${"
#   a NAME that is not [A-Za-z_][A-Za-z0-9_]* -> error "line N: bad variable name "NAME""
#                         (with the double quotes, e.g.  line 1: bad variable name "1X")
# Substituted values are NOT scanned again (a value containing "${APP}" stays literal).
# Errors go to stderr with exit 3, and NOTHING may be printed to stdout in that case
# (buffer the rendered lines and only print them once the whole template is fine).
# N is the template line number. Wrong argument count / unreadable file: usage, exit 2.
#
# HINT: one awk program. Read VARS_FILE in BEGIN with getline and split each line at
# index(line, "=") -- never with -F= (that would cut values containing '='). Do NOT use
# sub()/gsub() to insert values: '&' and '\' in the replacement are special there.
# Instead walk each line with index(s, "$"), building the output with substr() and
# string concatenation. Store rendered lines in an array, print them in END unless an
# error flag is set ("exit" inside a rule still runs END, so check the flag there).
#
# Check with -- vars.env:
#   # deployment settings
#   APP=billing
#   PORT=8080
#   EMPTY=
#   GREETING=Hello, world = hi
#   REGEXY=a&b\1 ${APP}
# and tpl.txt:
#   service ${APP} listens on :${PORT}
#   host=${HOST:-localhost} empty=[${EMPTY}] fallback=[${EMPTY:-none}]
#   price: $$5 and $5 and a lone $ sign
#   ${GREETING}
#   raw: ${REGEXY}
#   ${APP}${APP}-${PORT:-9}
#
#   ./template_render.sh vars.env < tpl.txt     -> exit 0, exactly:
#     service billing listens on :8080
#     host=localhost empty=[] fallback=[none]
#     price: $5 and $5 and a lone $ sign
#     Hello, world = hi
#     raw: a&b\1 ${APP}
#     billingbilling-8080
#   printf 'ok ${APP}\nbad ${NOPE}\n' | ./template_render.sh vars.env
#        -> NO stdout, stderr "line 2: undefined variable NOPE", exit 3
#   printf 'x ${APP\n' | ./template_render.sh vars.env
#        -> stderr "line 1: unterminated ${", exit 3
#   printf '${1X}\n' | ./template_render.sh vars.env
#        -> stderr 'line 1: bad variable name "1X"', exit 3
#   printf 'cost $${PORT}\n' | ./template_render.sh vars.env     -> "cost ${PORT}"
#   printf 'A=1\nnot an assignment\n' > badvars; echo hi | ./template_render.sh badvars
#        -> stderr "vars line 2: bad assignment", exit 2
#   ./template_render.sh                                         -> usage, exit 2

set -u

usage() { echo "usage: $0 VARS_FILE < template.txt" >&2; exit 2; }

[ "$#" -eq 1 ] || usage
[ -f "$1" ] && [ -r "$1" ] || usage

# Pass the file name through ENVIRON, not -v, so backslashes in it are not interpreted.
TPL_VARS_FILE="$1" exec awk '
function fail(code, msg) {
    if (!err) { print msg > "/dev/stderr"; err = code }
    exit
}
BEGIN {
    err = 0; nout = 0
    file = ENVIRON["TPL_VARS_FILE"]
    vn = 0
    while ((getline line < file) > 0) {
        vn++
        tmp = line
        sub(/^[ \t\r]+/, "", tmp)
        if (tmp == "" || substr(tmp, 1, 1) == "#") continue
        eq = index(line, "=")
        key = (eq > 0) ? substr(line, 1, eq - 1) : ""
        if (eq == 0 || key !~ /^[A-Za-z_][A-Za-z0-9_]*$/) {
            close(file)
            fail(2, "vars line " vn ": bad assignment")
        }
        val[key] = substr(line, eq + 1)
        def[key] = 1
    }
    close(file)
}
{
    s = $0; out = ""
    while ((p = index(s, "$")) > 0) {
        out = out substr(s, 1, p - 1)
        nxt = substr(s, p + 1, 1)
        if (nxt == "$") {                       # $$ -> $
            out = out "$"; s = substr(s, p + 2); continue
        }
        if (nxt != "{") {                       # any other $ is literal
            out = out "$"; s = substr(s, p + 1); continue
        }
        rest = substr(s, p + 2)
        close_at = index(rest, "}")
        if (close_at == 0) fail(3, "line " NR ": unterminated ${")
        inner = substr(rest, 1, close_at - 1)
        s = substr(rest, close_at + 1)
        dpos = index(inner, ":-")
        if (dpos > 0) {
            name = substr(inner, 1, dpos - 1)
            dflt = substr(inner, dpos + 2)
        } else {
            name = inner
        }
        if (name !~ /^[A-Za-z_][A-Za-z0-9_]*$/)
            fail(3, "line " NR ": bad variable name \"" name "\"")
        if (dpos > 0) {
            out = out ((name in def && val[name] != "") ? val[name] : dflt)
        } else {
            if (!(name in def)) fail(3, "line " NR ": undefined variable " name)
            out = out val[name]
        }
    }
    rendered[++nout] = out s
}
END {
    if (err) exit err
    for (i = 1; i <= nout; i++) print rendered[i]
}
'
