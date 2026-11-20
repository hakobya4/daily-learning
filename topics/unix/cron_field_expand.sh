#!/usr/bin/env bash
#
# Day 61, Task 5 -- Unix/shell: expand one crontab field into the concrete values it matches.
#
# THE PROBLEM
# ------------
# Usage: ./cron_field_expand.sh FIELD SPEC
# FIELD is one of: minute (0-59), hour (0-23), dom (1-31), month (1-12), dow (0-6).
# SPEC is a crontab field in the classic numeric syntax -- a comma-separated list whose
# items are:
#   *          every value of the field
#   N          a single value
#   A-B        an inclusive range (A <= B, otherwise invalid)
#   */S        every S-th value starting at the field minimum
#   A-B/S      every S-th value of the range, starting at A
#   N/S        every S-th value from N up to the field maximum
# S must be a positive integer (0 is invalid).
# Day of week accepts 7 as another name for Sunday (0): "7" -> 0, "5-7" -> 0,5,6.
# Print the matched values ONCE each, in ascending numeric order, comma-separated, on one
# line ("5,1-3,2" -> "1,2,3,5"). No names (JAN, MON), no "?", "L", "W" or "#".
# Invalid SPEC (out-of-range value, empty item, A > B, bad step, junk characters):
#   print "invalid FIELD spec: SPEC" to stderr and exit 1.
# Unknown FIELD or wrong number of arguments: a usage line on stderr, exit 2.
#
# HINT: one awk BEGIN block: split(spec, items, ","); for each item split off "/S",
# then decide the [a, b] range ("*" -> [lo, hi], "A-B", or "N" -> [N, N] or [N, hi] when
# a step was given), validate with regexes like /^[0-9]+$/, then loop v = a; v <= b;
# v += step and mark seen[v]. Finally walk lo..hi and print the marked values.
#
# Check with:
#   ./cron_field_expand.sh minute '*/15'     -> 0,15,30,45
#   ./cron_field_expand.sh hour 9-17/4       -> 9,13,17
#   ./cron_field_expand.sh minute 5,1-3,2    -> 1,2,3,5
#   ./cron_field_expand.sh minute 10/20      -> 10,30,50
#   ./cron_field_expand.sh month '*/5'       -> 1,6,11
#   ./cron_field_expand.sh dom 1,15,31       -> 1,15,31
#   ./cron_field_expand.sh dow 5-7           -> 0,5,6
#   ./cron_field_expand.sh dow 0,7           -> 0
#   ./cron_field_expand.sh dow '*/2'         -> 0,2,4,6
#   ./cron_field_expand.sh hour 23/5         -> 23
#   ./cron_field_expand.sh hour 25           -> stderr "invalid hour spec: 25", exit 1
#   ./cron_field_expand.sh minute 5-1        -> stderr "invalid minute spec: 5-1", exit 1
#   ./cron_field_expand.sh minute '*/0'      -> stderr "invalid minute spec: */0", exit 1
#   ./cron_field_expand.sh dom 0             -> stderr "invalid dom spec: 0", exit 1
#   ./cron_field_expand.sh minute ,1         -> stderr "invalid minute spec: ,1", exit 1
#   ./cron_field_expand.sh minute 1-2-3      -> stderr "invalid minute spec: 1-2-3", exit 1
#   ./cron_field_expand.sh week 1            -> usage on stderr, exit 2

# TODO: replace this line with your implementation
echo "not implemented" >&2
exit 1
