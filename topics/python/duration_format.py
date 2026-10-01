"""
Day 10, Task 2 -- Python: parse and format durations.

THE PROBLEM
------------
Write two functions:

  parse_duration(s: str) -> int
      Convert strings like "1h30m15s", "45m", "2h", "90s" to total
      seconds. Units are h, m, s, each optional, always in that order,
      each appearing at most once. Raise ValueError for an empty string
      or anything malformed ("abc", "1x", "5m1h", "10").

  format_duration(seconds: int) -> str
      The inverse: 5415 -> "1h30m15s". Omit zero units ("3600" -> "1h",
      "61" -> "1m1s"). 0 -> "0s". Raise ValueError if negative.

HOW TO WORK THROUGH THIS
-------------------------
A single anchored regex with three optional named groups does the
parsing; check for "no group matched" separately. divmod() does the
formatting.

Run: python3 duration_format.py
"""
import re  # noqa: F401


_DURATION_RE = re.compile(r"^(?:(?P<h>\d+)h)?(?:(?P<m>\d+)m)?(?:(?P<s>\d+)s)?$")


def parse_duration(s: str) -> int:
    m = _DURATION_RE.match(s)
    if not s or m is None or all(v is None for v in m.groupdict().values()):
        raise ValueError(f"malformed duration: {s!r}")
    h, mi, sec = (int(m.group(k) or 0) for k in "hms")
    return h * 3600 + mi * 60 + sec


def format_duration(seconds: int) -> str:
    if seconds < 0:
        raise ValueError("seconds must be >= 0")
    if seconds == 0:
        return "0s"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return "".join(f"{v}{u}" for v, u in ((h, "h"), (m, "m"), (s, "s")) if v)


def _run_tests() -> None:
    assert parse_duration("1h30m15s") == 5415
    assert parse_duration("45m") == 2700
    assert parse_duration("2h") == 7200
    assert parse_duration("90s") == 90
    assert parse_duration("1h5s") == 3605
    for bad in ["", "abc", "1x", "5m1h", "10", "1h1h", "h"]:
        try:
            parse_duration(bad)
            assert False, f"should reject {bad!r}"
        except ValueError:
            pass

    assert format_duration(5415) == "1h30m15s"
    assert format_duration(3600) == "1h"
    assert format_duration(61) == "1m1s"
    assert format_duration(0) == "0s"
    assert format_duration(7325) == "2h2m5s"
    try:
        format_duration(-1)
        assert False, "should reject negative"
    except ValueError:
        pass
    for n in [0, 1, 59, 60, 3599, 3600, 86399, 100000]:
        assert parse_duration(format_duration(n)) == n
    print("All duration_format tests passed.")


if __name__ == "__main__":
    _run_tests()
