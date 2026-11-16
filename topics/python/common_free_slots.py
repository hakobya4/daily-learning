"""
Day 56, Task 10 -- Python: common free meeting slots across several calendars.

THE PROBLEM
------------
Each person's calendar is a list of busy intervals "HH:MM-HH:MM" (end exclusive, same
day, NOT necessarily sorted, may overlap each other). Given:

  calendars      -- list of per-person lists of busy strings
  work_start     -- "HH:MM", start of the working day (the same for everybody)
  work_end       -- "HH:MM", end of the working day
  min_minutes    -- minimum slot length (int, > 0)

return every maximal time window inside [work_start, work_end) in which NOBODY is busy
and whose length is >= min_minutes, as a sorted list of "HH:MM-HH:MM" strings.

Rules:
  * Busy intervals may start before work_start or end after work_end -- clip them.
  * A busy interval with start >= end, or any malformed time (not two digits ':' two
    digits, hour 0..23, minute 0..59; "24:00" IS allowed but only as an END time / as
    work_end), raises ValueError. work_start >= work_end also raises ValueError.
  * Touching busy intervals ("09:00-10:00" and "10:00-11:00") leave no gap between them.
  * An empty calendars list means everyone (nobody) is free all day.

Also implement first_slot(calendars, work_start, work_end, minutes): the EARLIEST
"HH:MM-HH:MM" window of EXACTLY `minutes` length that fits in a common free gap, or None.

Example:
  free_slots([["09:00-10:30", "12:00-13:00"], ["10:00-11:00", "15:00-16:00"]],
             "09:00", "17:00", 30)
      -> ["11:00-12:00", "13:00-15:00", "16:00-17:00"]
  first_slot(same, "09:00", "17:00", 90) -> "13:00-14:30"

Hint: convert everything to minutes since midnight, throw all people's intervals into ONE
list, sort by start, merge (like merge_intervals), then walk the merged list collecting
the gaps between work_start, each merged block, and work_end.

Run: python3 common_free_slots.py
"""


import re

_TIME_RE = re.compile(r"^(\d{2}):(\d{2})$")


def _to_min(t, allow_24=False):
    m = _TIME_RE.match(t) if isinstance(t, str) else None
    if not m:
        raise ValueError("malformed time %r" % (t,))
    h, mi = int(m.group(1)), int(m.group(2))
    if h == 24 and mi == 0 and allow_24:
        return 1440
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ValueError("time out of range %r" % (t,))
    return h * 60 + mi


def _fmt(m):
    return "%02d:%02d" % divmod(m, 60)


def _gaps(calendars, work_start, work_end):
    ws = _to_min(work_start)
    we = _to_min(work_end, allow_24=True)
    if ws >= we:
        raise ValueError("work_start must be before work_end")
    intervals = []
    for person in calendars:
        for busy in person:
            parts = busy.split("-") if isinstance(busy, str) else []
            if len(parts) != 2:
                raise ValueError("malformed interval %r" % (busy,))
            s, e = _to_min(parts[0]), _to_min(parts[1], allow_24=True)
            if s >= e:
                raise ValueError("empty or reversed interval %r" % (busy,))
            s, e = max(s, ws), min(e, we)
            if s < e:
                intervals.append((s, e))
    intervals.sort()
    gaps, cur = [], ws
    for s, e in intervals:
        if s > cur:
            gaps.append((cur, s))
        cur = max(cur, e)
    if cur < we:
        gaps.append((cur, we))
    return gaps


def free_slots(calendars, work_start, work_end, min_minutes):
    return [_fmt(s) + "-" + _fmt(e)
            for s, e in _gaps(calendars, work_start, work_end) if e - s >= min_minutes]


def first_slot(calendars, work_start, work_end, minutes):
    for s, e in _gaps(calendars, work_start, work_end):
        if e - s >= minutes:
            return _fmt(s) + "-" + _fmt(s + minutes)
    return None


def _run_tests():
    cals = [["09:00-10:30", "12:00-13:00"], ["10:00-11:00", "15:00-16:00"]]
    assert free_slots(cals, "09:00", "17:00", 30) == \
        ["11:00-12:00", "13:00-15:00", "16:00-17:00"]
    assert free_slots(cals, "09:00", "17:00", 61) == ["13:00-15:00"]
    assert first_slot(cals, "09:00", "17:00", 90) == "13:00-14:30"
    assert first_slot(cals, "09:00", "17:00", 60) == "11:00-12:00"
    assert first_slot(cals, "09:00", "17:00", 121) is None

    # Nobody busy / empty calendars.
    assert free_slots([], "08:00", "18:00", 15) == ["08:00-18:00"]
    assert free_slots([[], []], "08:00", "18:00", 15) == ["08:00-18:00"]

    # Unsorted + overlapping + touching + clipping.
    cals2 = [["13:00-14:00", "07:00-09:30"], ["09:30-10:00", "13:30-15:00"],
             ["16:45-19:00"]]
    assert free_slots(cals2, "09:00", "17:00", 1) == ["10:00-13:00", "15:00-16:45"]
    assert free_slots(cals2, "09:00", "17:00", 106) == ["10:00-13:00"]

    # Busy all day.
    assert free_slots([["00:00-24:00"]], "09:00", "17:00", 1) == []
    assert first_slot([["00:00-24:00"]], "09:00", "17:00", 1) is None

    # 24:00 as work_end; exact-length slot is kept.
    assert free_slots([["00:00-23:30"]], "00:00", "24:00", 30) == ["23:30-24:00"]

    # Validation.
    for bad in (
        lambda: free_slots([["10:00-09:00"]], "09:00", "17:00", 10),
        lambda: free_slots([["10:00-10:00"]], "09:00", "17:00", 10),
        lambda: free_slots([["9:00-10:00"]], "09:00", "17:00", 10),
        lambda: free_slots([["09:60-10:00"]], "09:00", "17:00", 10),
        lambda: free_slots([["24:00-24:00"]], "09:00", "17:00", 10),
        lambda: free_slots([["09:00 10:00"]], "09:00", "17:00", 10),
        lambda: free_slots([], "17:00", "09:00", 10),
        lambda: free_slots([], "24:00", "24:00", 10),
    ):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")

    # Brute-force cross-check on random calendars (minute-by-minute occupancy).
    import random
    rng = random.Random(56)

    def fmt(m):
        return "%02d:%02d" % divmod(m, 60)

    for _ in range(200):
        cals = []
        busy = [False] * 1440
        for _p in range(rng.randint(0, 4)):
            person = []
            for _i in range(rng.randint(0, 4)):
                s = rng.randrange(0, 1430, 5)
                e = rng.randrange(s + 5, min(1440, s + 240) + 1, 5)
                person.append(fmt(s) + "-" + fmt(e))
                for m in range(s, e):
                    busy[m] = True
            cals.append(person)
        ws, we = 8 * 60, 18 * 60
        mn = rng.choice([5, 15, 30, 60])
        exp, m = [], ws
        while m < we:
            if busy[m]:
                m += 1
                continue
            s = m
            while m < we and not busy[m]:
                m += 1
            if m - s >= mn:
                exp.append(fmt(s) + "-" + fmt(m))
        assert free_slots(cals, "08:00", "18:00", mn) == exp, cals
        fs = first_slot(cals, "08:00", "18:00", mn)
        if exp:
            start = exp[0].split("-")[0]
            h, mm = map(int, start.split(":"))
            assert fs == start + "-" + fmt(h * 60 + mm + mn)
        else:
            assert fs is None

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
