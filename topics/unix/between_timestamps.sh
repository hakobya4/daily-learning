#!/usr/bin/env bash
#
# Day 54, Task 5 -- Unix/shell: log lines inside an inclusive ISO-timestamp window.
#
# THE PROBLEM
# ------------
# Usage: ./between_timestamps.sh START END FILE
# START and END are ISO-8601 timestamps of the exact form YYYY-MM-DDTHH:MM:SS
# (e.g. 2026-11-14T09:30:00). Each log line in FILE is expected to START with a timestamp
# of the same form followed by a space and the message.
# Print, in file order, every line whose timestamp t satisfies START <= t <= END.
# Lines that do not begin with a well-formed timestamp are skipped. After processing, print
# "skipped N" to STDERR where N is the number of such skipped lines (print it even if N is 0).
# Exit 1 (usage message on stderr) if: the argument count is wrong, FILE is not a readable
# regular file, START or END is not well-formed, or START > END.
#
# HINT: fixed-width ISO timestamps sort correctly as plain STRINGS, so no date parsing is
# needed -- awk's string comparison ("a" <= "b") on $1 does the job. Validate the shape with
# a regex such as ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$ (use [[ =~ ]] in
# bash for the arguments, and the same regex in awk for $1). Make sure awk compares strings,
# not numbers (concatenate "" if in doubt). Write the count with  print ... > "/dev/stderr".
#
# Check with:
#   printf '%s\n' '2026-11-14T08:59:59 boot' '2026-11-14T09:00:00 start' 'garbage line' \
#     '2026-11-14T09:15:30 work' '2026-11-14T10:00:00 lunch' '2026-11-14T10:00:01 late' \
#     '2026-11-14 09:20:00 wrong-format' > /tmp/d54.log
#   ./between_timestamps.sh 2026-11-14T09:00:00 2026-11-14T10:00:00 /tmp/d54.log
# Expected stdout:
#   2026-11-14T09:00:00 start
#   2026-11-14T09:15:30 work
#   2026-11-14T10:00:00 lunch
# Expected stderr:
#   skipped 2
#
#   ./between_timestamps.sh 2026-11-14T10:00:00 2026-11-14T09:00:00 /tmp/d54.log; echo $?
# Expected: a usage message on stderr, then 1

if [ "$#" -ne 3 ] || [ ! -f "$3" ] || [ ! -r "$3" ]; then
    echo "usage: $0 START END FILE" >&2
    exit 1
fi

ts_re='^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$'
if ! [[ $1 =~ $ts_re ]] || ! [[ $2 =~ $ts_re ]] || [[ $1 > $2 ]]; then
    echo "usage: $0 START END FILE  (YYYY-MM-DDTHH:MM:SS, START <= END)" >&2
    exit 1
fi

awk -v start="$1" -v end="$2" '
BEGIN { skipped = 0 }
{
    ts = substr($0, 1, 19) ""
    rest = substr($0, 20, 1)
    if (ts !~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$/ || (rest != " " && rest != "")) {
        skipped++
        next
    }
    if (ts >= start "" && ts <= end "")
        print
}
END { print "skipped " skipped > "/dev/stderr" }
' "$3"
