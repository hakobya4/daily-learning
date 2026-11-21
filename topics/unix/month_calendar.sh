#!/usr/bin/env bash
#
# Day 62, Task 6 -- Unix/shell: print a month calendar grid WITHOUT `cal` or `date`
# (day-of-week arithmetic and Gregorian leap years by hand).
#
# THE PROBLEM
# ------------
# Usage: ./month_calendar.sh [-s] YEAR MONTH
# Print the calendar of MONTH (1-12) of YEAR (1-9999, proleptic Gregorian calendar --
# no 1752 Julian switch-over) in exactly this format, weeks starting on MONDAY:
#
#      November 2026
#   Mo Tu We Th Fr Sa Su
#                      1
#    2  3  4  5  6  7  8
#    9 10 11 12 13 14 15
#   16 17 18 19 20 21 22
#   23 24 25 26 27 28 29
#   30
#
#   - line 1: "<Monthname> <YEAR>" (English name, YEAR without leading zeros) left-padded
#     with floor((20 - length) / 2) spaces, i.e. centered over the 20-char grid,
#     rounding the extra space to the RIGHT (which is then trimmed, see below);
#   - line 2: the weekday header;
#   - then one line per week: each day right-aligned in 2 characters, cells separated
#     by one space, blank cells (before day 1) are two spaces;
#   - NO trailing whitespace on any line, no blank line at the end, and only as many
#     week lines as the month needs (February 2021 has exactly 4).
# -s: weeks start on SUNDAY instead (header "Su Mo Tu We Th Fr Sa").
# Leap years: divisible by 4, except centuries, except multiples of 400
# (2000 and 2024 are leap, 1900 and 2026 are not).
# Bad arguments (non-numeric, month outside 1-12, year outside 1-9999, wrong count):
#   a usage line on stderr, exit 2.
# Do NOT call `cal`, `ncal` or `date` -- compute the weekday yourself.
#
# HINT: Sakamoto's method gives the weekday (0 = Sunday) of any Gregorian date:
#   t = (0 3 2 5 0 3 5 1 4 6 2 4);  if (m < 3) y -= 1
#   dow = (y + y/4 - y/100 + y/400 + t[m-1] + d) % 7      (integer division)
# Convert to a Monday-first column with (dow + 6) % 7. Do it all in one awk BEGIN
# block (awk's int() for integer division) or in bash $(( )) arithmetic, build each
# week line in a string and strip trailing spaces before printing (sub(/ +$/, "")).
#
# Check with:
#   ./month_calendar.sh 2026 11         -> the grid above
#   ./month_calendar.sh 2021 2          ->
#        February 2021
#     Mo Tu We Th Fr Sa Su
#      1  2  3  4  5  6  7
#      8  9 10 11 12 13 14
#     15 16 17 18 19 20 21
#     22 23 24 25 26 27 28
#   ./month_calendar.sh 2024 2          -> last line "26 27 28 29"; first week line
#                                           "          1  2  3  4"
#   ./month_calendar.sh 1900 2          -> last line "26 27 28" (1900 is NOT leap);
#                                           first week line "          1  2  3  4"
#   ./month_calendar.sh 2000 2          -> first week line "    1  2  3  4  5  6",
#                                           last line "28 29"
#   ./month_calendar.sh 2027 8          -> title line "    August 2027", last line "30 31"
#   ./month_calendar.sh 1752 9          -> first week line "             1  2  3"
#                                           (proleptic Gregorian: Sept 1 1752 = Friday),
#                                           last line "25 26 27 28 29 30"
#   ./month_calendar.sh -s 2026 11      ->
#        November 2026
#     Su Mo Tu We Th Fr Sa
#      1  2  3  4  5  6  7
#      8  9 10 11 12 13 14
#     15 16 17 18 19 20 21
#     22 23 24 25 26 27 28
#     29 30
#   ./month_calendar.sh -s 2021 2       -> first week line "    1  2  3  4  5  6", last "28"
#   ./month_calendar.sh 2026 13         -> usage on stderr, exit 2
#   ./month_calendar.sh 2026            -> usage on stderr, exit 2
#   ./month_calendar.sh 0 5             -> usage on stderr, exit 2
# Bonus check if you have Python: python3 -c "import calendar" can tell you the
# weekday of day 1 (calendar.weekday(y, m, 1), Monday = 0) for random months.

# TODO: replace this line with your implementation
echo "not implemented" >&2
exit 1
