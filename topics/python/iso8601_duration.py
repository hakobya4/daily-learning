"""
Day 63, Task 2 -- Python: ISO 8601 durations -- parse, format canonically, and add to dates
with calendar-aware month arithmetic.

THE PROBLEM
------------
Durations like "P1Y2M10DT2H30M" show up in YouTube APIs, cron-like schedulers, iCalendar
(RFC 5545) and XML Schema. Implement them WITHOUT third-party libraries (no dateutil,
no isodate, no regex-free "just use a library" shortcuts -- the `re` module is fine).

A duration is represented as a dict with exactly these integer keys:
    {"years", "months", "weeks", "days", "hours", "minutes", "seconds"}

1) parse_duration(s) -> dict
   Grammar (strict, uppercase only):
       [-]P[nY][nM][nW][nD][T[nH][nM][nS]]
   - "P" is mandatory; components must appear in exactly that order; each at most once.
   - n is one or more ASCII digits (no sign, no fraction, no spaces).
   - "T" must be present iff at least one of H/M/S follows it ("P1DT" and "PT" are invalid);
     the M before T means months, the M after T means minutes.
   - At least one component overall ("P" and "-P" are invalid).
   - A leading "-" negates EVERY component (so "-P1DT2H" -> days=-1, hours=-2).
   - Missing components are 0.
   Anything else -> raise ValueError.

2) format_duration(d) -> str
   The inverse, canonical form: omit zero components, emit in grammar order, add "T" only
   when a time component is non-zero, and the all-zero duration is "PT0S".
   If ALL non-zero components are negative, emit a leading "-" and the absolute values.
   Mixed signs (e.g. days=1, hours=-2) cannot be written in this grammar -> ValueError.
   Do NOT normalise (90 minutes stays "PT90M", not "PT1H30M").

3) add_duration(dt, d) -> datetime
   Calendar-aware addition, in this order:
     a) add years*12 + months to the month; if the day does not exist in the target month,
        CLAMP to the last day of that month (Jan 31 + P1M -> Feb 28 or 29);
     b) then add weeks*7 + days as calendar days;
     c) then add hours/minutes/seconds as an exact timedelta.
   Works for negative durations too (Mar 31 + "-P1M" -> Feb 28/29). Naive datetimes only.
   Hint: compute total = dt.year*12 + (dt.month-1) + months_to_add, then divmod by 12;
   calendar.monthrange(year, month)[1] gives the number of days in a month.

4) fixed_seconds(d) -> int
   Total length in seconds when that is well defined, i.e. years == months == 0
   (a week is 7*86400 s and a day is 86400 s here -- ignore DST). If years or months are
   non-zero raise ValueError ("P1M" has no fixed length).

Run: python3 iso8601_duration.py
"""

from datetime import datetime

KEYS = ("years", "months", "weeks", "days", "hours", "minutes", "seconds")


import calendar
import re
from datetime import timedelta

_DUR_RE = re.compile(
    r"(-)?P"
    r"(?:([0-9]+)Y)?(?:([0-9]+)M)?(?:([0-9]+)W)?(?:([0-9]+)D)?"
    r"(?:(T)(?:([0-9]+)H)?(?:([0-9]+)M)?(?:([0-9]+)S)?)?"
)


def parse_duration(s):
    if not isinstance(s, str):
        raise ValueError("duration must be a string")
    m = _DUR_RE.fullmatch(s)
    if m is None:
        raise ValueError(f"invalid ISO 8601 duration: {s!r}")
    neg, y, mo, w, d, t, h, mi, sec = m.groups()
    date_parts = (y, mo, w, d)
    time_parts = (h, mi, sec)
    if t is not None and all(p is None for p in time_parts):
        raise ValueError(f"'T' must be followed by a time component: {s!r}")
    if all(p is None for p in date_parts + time_parts):
        raise ValueError(f"duration has no components: {s!r}")
    sign = -1 if neg else 1
    values = [sign * int(p) if p is not None else 0 for p in date_parts + time_parts]
    return dict(zip(KEYS, values))


def format_duration(d):
    vals = [int(d.get(k, 0)) for k in KEYS]
    nonzero = [v for v in vals if v != 0]
    if not nonzero:
        return "PT0S"
    if all(v < 0 for v in nonzero):
        sign = "-"
    elif all(v > 0 for v in nonzero):
        sign = ""
    else:
        raise ValueError("mixed-sign durations cannot be represented")
    vals = [abs(v) for v in vals]
    out = [sign, "P"]
    for v, unit in zip(vals[:4], "YMWD"):
        if v:
            out.append(f"{v}{unit}")
    if any(vals[4:]):
        out.append("T")
        for v, unit in zip(vals[4:], "HMS"):
            if v:
                out.append(f"{v}{unit}")
    return "".join(out)


def add_duration(dt, d):
    months = d.get("years", 0) * 12 + d.get("months", 0)
    total = dt.year * 12 + (dt.month - 1) + months
    year, month0 = divmod(total, 12)
    month = month0 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    out = dt.replace(year=year, month=month, day=day)
    out = out + timedelta(days=d.get("weeks", 0) * 7 + d.get("days", 0))
    out = out + timedelta(hours=d.get("hours", 0), minutes=d.get("minutes", 0),
                          seconds=d.get("seconds", 0))
    return out


def fixed_seconds(d):
    if d.get("years", 0) or d.get("months", 0):
        raise ValueError("durations with years or months have no fixed length")
    return (d.get("weeks", 0) * 7 * 86400 + d.get("days", 0) * 86400
            + d.get("hours", 0) * 3600 + d.get("minutes", 0) * 60 + d.get("seconds", 0))


def _run_tests():
    def D(**kw):
        out = dict.fromkeys(KEYS, 0)
        out.update(kw)
        return out

    # --- parsing ---
    assert parse_duration("P1Y2M10DT2H30M") == D(years=1, months=2, days=10, hours=2, minutes=30)
    assert parse_duration("PT36H") == D(hours=36)
    assert parse_duration("P3W") == D(weeks=3)
    assert parse_duration("P1M") == D(months=1)
    assert parse_duration("PT1M") == D(minutes=1)
    assert parse_duration("P0D") == D()
    assert parse_duration("PT0S") == D()
    assert parse_duration("P2W3DT4S") == D(weeks=2, days=3, seconds=4)
    assert parse_duration("-P1DT2H") == D(days=-1, hours=-2)
    assert parse_duration("P0010Y") == D(years=10)
    assert parse_duration("PT90M") == D(minutes=90)
    for bad in ["", "P", "-P", "PT", "P1DT", "1D", "P1D2H", "PT2D", "P1H", "P1M1Y",
                "P1Y1Y", "PT1S1M", "P-1D", "P1.5D", "p1d", "P1d", "P 1D", "+P1D", "--P1D",
                "P1DT1H1M1S1", "PT1H ", " P1D", "P1W1W", "PTT1H", "P1YT", "P1Y2MT"]:
        try:
            parse_duration(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"parse_duration should reject {bad!r}")

    # --- formatting ---
    assert format_duration(D(years=1, months=2, days=10, hours=2, minutes=30)) == "P1Y2M10DT2H30M"
    assert format_duration(D()) == "PT0S"
    assert format_duration(D(minutes=90)) == "PT90M"
    assert format_duration(D(months=1)) == "P1M"
    assert format_duration(D(minutes=1)) == "PT1M"
    assert format_duration(D(weeks=2, seconds=5)) == "P2WT5S"
    assert format_duration(D(days=-1, hours=-2)) == "-P1DT2H"
    try:
        format_duration(D(days=1, hours=-2))
    except ValueError:
        pass
    else:
        raise AssertionError("mixed signs must be rejected")
    for s in ["P1Y2M10DT2H30M", "PT36H", "P3W", "-P4DT5M", "P1Y", "PT1S", "P2W3DT4H5M6S"]:
        assert format_duration(parse_duration(s)) == s, s

    # --- calendar-aware addition ---
    dt = datetime
    assert add_duration(dt(2026, 1, 31), parse_duration("P1M")) == dt(2026, 2, 28)
    assert add_duration(dt(2024, 1, 31), parse_duration("P1M")) == dt(2024, 2, 29)
    assert add_duration(dt(2024, 2, 29), parse_duration("P1Y")) == dt(2025, 2, 28)
    assert add_duration(dt(2026, 3, 31), parse_duration("-P1M")) == dt(2026, 2, 28)
    assert add_duration(dt(2026, 11, 22), parse_duration("P2M")) == dt(2027, 1, 22)
    assert add_duration(dt(2026, 1, 15), parse_duration("-P13M")) == dt(2024, 12, 15)
    # months first, THEN days: Jan 31 + 1 month = Feb 28, + 1 day = Mar 1
    assert add_duration(dt(2026, 1, 31), parse_duration("P1M1D")) == dt(2026, 3, 1)
    assert add_duration(dt(2026, 11, 22, 23, 0), parse_duration("PT90M")) == dt(2026, 11, 23, 0, 30)
    assert add_duration(dt(2026, 12, 31, 12), parse_duration("P1W1DT12H")) == dt(2027, 1, 9)
    assert add_duration(dt(2026, 3, 1), parse_duration("-PT1S")) == dt(2026, 2, 28, 23, 59, 59)
    assert add_duration(dt(2000, 2, 29), parse_duration("P100Y")) == dt(2100, 2, 28)
    assert add_duration(dt(2026, 5, 31, 8, 15, 30), parse_duration("P0D")) == dt(2026, 5, 31, 8, 15, 30)
    # adding then subtracting a month is NOT always the identity -- that is expected
    assert add_duration(add_duration(dt(2026, 1, 31), parse_duration("P1M")),
                        parse_duration("-P1M")) == dt(2026, 1, 28)

    # --- fixed length ---
    assert fixed_seconds(parse_duration("PT36H")) == 129600
    assert fixed_seconds(parse_duration("P1W2DT3H4M5S")) == 9 * 86400 + 3 * 3600 + 4 * 60 + 5
    assert fixed_seconds(parse_duration("-P1D")) == -86400
    assert fixed_seconds(parse_duration("PT0S")) == 0
    for s in ("P1M", "P1Y", "-P2Y3D"):
        try:
            fixed_seconds(parse_duration(s))
        except ValueError:
            pass
        else:
            raise AssertionError(f"fixed_seconds should reject {s}")

    print("all iso8601_duration tests passed")


if __name__ == "__main__":
    _run_tests()
