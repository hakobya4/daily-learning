"""
Day 58, Task 10 -- Python: parse a 5-field cron expression and compute its next run time.

THE PROBLEM
------------
Implement next_run(expr, after) -> datetime | None.

`expr` is a classic 5-field cron expression "MIN HOUR DOM MON DOW" (fields separated
by one or more spaces):
    MIN  0-59    HOUR 0-23    DOM 1-31    MON 1-12    DOW 0-7 (0 and 7 both = Sunday)
Each field is a comma-separated list of items; each item is one of
    *          every value in range
    N          a single value
    A-B        an inclusive range (A <= B required)
    */S        every S-th value starting at the range minimum   (S >= 1)
    A-B/S      every S-th value from A to B
    N/S        every S-th value from N to the field maximum      (e.g. 5/15 = 5,20,35,50)
Anything else (wrong field count, out-of-range numbers, A > B, S = 0, empty items,
names like "MON"/"JAN", "@daily", ...) raises ValueError.

Day matching follows Vixie cron: if BOTH the DOM and DOW fields are restricted (i.e.
the field text is not exactly "*"), a day matches when EITHER matches; if one of them
is "*", only the other one matters.

next_run returns the earliest minute-aligned datetime STRICTLY AFTER `after`
(seconds/microseconds of `after` are ignored: from 10:15:30 the first candidate is
10:16:00). Naive datetimes only, no time zones / DST. If no match exists within the
next 5 years (e.g. "0 0 30 2 *"), return None.

Example (2026-11-18 is a Wednesday):
  next_run("*/15 * * * *",   datetime(2026, 11, 18, 10, 7))    -> 2026-11-18 10:15
  next_run("0 9 * * 1-5",    datetime(2026, 11, 20, 9, 0))     -> 2026-11-23 09:00  (Fri -> Mon)
  next_run("30 2 29 2 *",    datetime(2026, 1, 1))             -> 2028-02-29 02:30
  next_run("0 0 13 * 5",     datetime(2026, 11, 18))           -> 2026-11-20 00:00  (a Friday: DOW wins)

Hint: parse each field into a SET of allowed ints (map DOW 7 -> 0; Python's
weekday() is Mon=0, so cron_dow = (d.weekday() + 1) % 7). Don't step minute by minute
for 5 years: advance by day while the date doesn't match, then by hour, then by minute
(reset the smaller units to their minimum each time you advance a larger one).

Run: python3 cron_next_run.py
"""

from datetime import datetime, timedelta


import re as _re

_FIELD_RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 7)]
_DIGITS = _re.compile(r"[0-9]+\Z")


def _number(tok, lo, hi):
    if not _DIGITS.match(tok):
        raise ValueError("bad number %r" % (tok,))
    v = int(tok)
    if not lo <= v <= hi:
        raise ValueError("%d out of range %d-%d" % (v, lo, hi))
    return v


def _parse_field(text, lo, hi):
    values = set()
    for item in text.split(","):
        if not item:
            raise ValueError("empty list item in %r" % (text,))
        step = 1
        has_step = "/" in item
        if has_step:
            base, step_text = item.split("/", 1)
            if not _DIGITS.match(step_text):
                raise ValueError("bad step in %r" % (item,))
            step = int(step_text)
            if step < 1:
                raise ValueError("step must be >= 1 in %r" % (item,))
        else:
            base = item
        if base == "*":
            a, b = lo, hi
        elif "-" in base:
            parts = base.split("-")
            if len(parts) != 2:
                raise ValueError("bad range %r" % (base,))
            a, b = _number(parts[0], lo, hi), _number(parts[1], lo, hi)
            if a > b:
                raise ValueError("range start > end in %r" % (base,))
        else:
            a = _number(base, lo, hi)
            b = hi if has_step else a
        values.update(range(a, b + 1, step))
    return values


def _parse(expr):
    if not isinstance(expr, str):
        raise ValueError("expression must be a string")
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError("expected 5 fields, got %d" % len(fields))
    sets = [_parse_field(f, lo, hi) for f, (lo, hi) in zip(fields, _FIELD_RANGES)]
    sets[4] = {d % 7 for d in sets[4]}           # 7 and 0 are both Sunday
    return sets, fields[2] != "*", fields[4] != "*"


def next_run(expr, after):
    (mins, hours, doms, months, dows), dom_restricted, dow_restricted = _parse(expr)

    def day_ok(t):
        dom_ok = t.day in doms
        dow_ok = (t.weekday() + 1) % 7 in dows
        if dom_restricted and dow_restricted:
            return dom_ok or dow_ok
        return dom_ok and dow_ok

    t = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
    try:
        limit = after.replace(year=after.year + 5)
    except ValueError:                           # after is Feb 29
        limit = after.replace(year=after.year + 5, day=28)
    while t <= limit:
        if t.month not in months or not day_ok(t):
            t = datetime(t.year, t.month, t.day) + timedelta(days=1)
        elif t.hour not in hours:
            t = t.replace(minute=0) + timedelta(hours=1)
        elif t.minute not in mins:
            t += timedelta(minutes=1)
        else:
            return t
    return None


def _brute(expr, after, limit_minutes):
    # Slow, naive reference (assumes a VALID expr): skips non-matching days, then tests
    # every minute of a matching day. Independent of your parser.
    f = expr.split()

    def expand(field, lo, hi):
        vals = set()
        for item in field.split(","):
            step = 1
            if "/" in item:
                item, step = item.split("/")
                step = int(step)
            if item == "*":
                a, b = lo, hi
            elif "-" in item:
                a, b = map(int, item.split("-"))
            else:
                a = int(item)
                b = hi if step != 1 else a
            vals.update(range(a, b + 1, step))
        return vals

    mi, ho, dm, mo, dw = (expand(f[0], 0, 59), expand(f[1], 0, 23), expand(f[2], 1, 31),
                          expand(f[3], 1, 12), {d % 7 for d in expand(f[4], 0, 7)})
    t = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
    end = t + timedelta(minutes=limit_minutes)
    while t < end:
        dom_ok, dow_ok = t.day in dm, (t.weekday() + 1) % 7 in dw
        if f[2] != "*" and f[4] != "*":
            day_ok = dom_ok or dow_ok
        else:
            day_ok = dom_ok and dow_ok
        if not (day_ok and t.month in mo):
            t = (t + timedelta(days=1)).replace(hour=0, minute=0)
            continue
        if t.minute in mi and t.hour in ho:
            return t
        t += timedelta(minutes=1)
    return "none-in-horizon"


def _run_tests():
    D = datetime
    assert next_run("*/15 * * * *", D(2026, 11, 18, 10, 7)) == D(2026, 11, 18, 10, 15)
    assert next_run("0 9 * * 1-5", D(2026, 11, 20, 9, 0)) == D(2026, 11, 23, 9, 0)
    assert next_run("30 2 29 2 *", D(2026, 1, 1)) == D(2028, 2, 29, 2, 30)
    assert next_run("0 0 13 * 5", D(2026, 11, 18)) == D(2026, 11, 20, 0, 0)
    assert next_run("* * * * *", D(2026, 12, 31, 23, 59, 59)) == D(2027, 1, 1, 0, 0)
    assert next_run("* * * * *", D(2026, 5, 5, 10, 15, 30)) == D(2026, 5, 5, 10, 16)
    assert next_run("0 0 1 1 *", D(2026, 1, 1, 0, 0)) == D(2027, 1, 1, 0, 0)
    assert next_run("5/20 * * * *", D(2026, 3, 3, 3, 46)) == D(2026, 3, 3, 4, 5)
    assert next_run("0 12 * * 7", D(2026, 11, 18)) == D(2026, 11, 22, 12, 0)   # 7 = Sunday
    assert next_run("0 12 * * 0", D(2026, 11, 18)) == D(2026, 11, 22, 12, 0)
    assert next_run("0 0 31 * *", D(2026, 4, 1)) == D(2026, 5, 31, 0, 0)       # April has 30
    assert next_run("0 0 30 2 *", D(2026, 1, 1)) is None
    assert next_run("15,45 8-10/2 * 6-8 *", D(2026, 1, 1)) == D(2026, 6, 1, 8, 15)
    assert next_run("0  0   *  *  *", D(2026, 1, 1, 0, 0)) == D(2026, 1, 2, 0, 0)

    for bad in ["* * * *", "* * * * * *", "60 * * * *", "* 24 * * *", "* * 0 * *",
                "* * 32 * *", "* * * 13 *", "* * * * 8", "5-1 * * * *", "*/0 * * * *",
                "1,,2 * * * *", "MON * * * *", "* * * JAN *", "@daily", "-1 * * * *",
                "a * * * *", "1-2-3 * * * *", "*/ * * * *", ""]:
        try:
            next_run(bad, D(2026, 1, 1))
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)

    import random
    rng = random.Random(58)
    pool = ["*", "*/7", "3", "10-20", "0-59/13", "1,2,3", "5/10"]
    for _ in range(300):
        expr = " ".join([rng.choice(pool), rng.choice(["*", "1-23/5", "4", "0,12"]),
                         rng.choice(["*", "1-10", "15", "*/9"]),
                         rng.choice(["*", "1-12/3", "11", "2"]),
                         rng.choice(["*", "1-5", "0", "6,7"])])
        start = D(2026, 1, 1) + timedelta(minutes=rng.randint(0, 400_000))
        expected = _brute(expr, start, 60 * 24 * 400)
        if expected == "none-in-horizon":
            continue
        assert next_run(expr, start) == expected, (expr, start)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
