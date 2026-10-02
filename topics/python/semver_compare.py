"""
Day 11, Task 10 -- Python: compare semantic versions.

THE PROBLEM
------------
Write compare_versions(a: str, b: str) -> int returning -1, 0 or 1
following semver 2.0 precedence for "MAJOR.MINOR.PATCH[-prerelease]":

  - Compare MAJOR, MINOR, PATCH numerically ("1.10.0" > "1.9.0").
  - A version WITH a prerelease is LOWER than the same without
    ("1.0.0-rc.1" < "1.0.0").
  - Prerelease identifiers are dot-separated and compared left to right:
      * numeric identifiers compare numerically;
      * alphanumeric ones compare lexically (ASCII);
      * numeric < alphanumeric;
      * if all shared identifiers are equal, the one with MORE
        identifiers is higher ("1.0.0-alpha" < "1.0.0-alpha.1").
  - Raise ValueError for anything not matching the shape (e.g. "1.0",
    "1.a.0", "").

Then write sort_versions(versions: list[str]) -> list[str], ascending,
using functools.cmp_to_key.

HOW TO WORK THROUGH THIS
-------------------------
Parse into (major, minor, patch, prerelease_tuple) first, validating
with a regex; then compare the pieces.

Run: python3 semver_compare.py
"""
import functools  # noqa: F401
import re  # noqa: F401


_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def _parse(v: str):
    m = _SEMVER.match(v) if isinstance(v, str) else None
    if not m:
        raise ValueError(f"invalid version: {v!r}")
    major, minor, patch, pre = m.groups()
    ids = tuple(pre.split(".")) if pre else ()
    return int(major), int(minor), int(patch), ids


def _cmp(x, y):
    return (x > y) - (x < y)


def compare_versions(a: str, b: str) -> int:
    pa, pb = _parse(a), _parse(b)
    c = _cmp(pa[:3], pb[:3])
    if c:
        return c
    ia, ib = pa[3], pb[3]
    if not ia and not ib:
        return 0
    if not ia:
        return 1
    if not ib:
        return -1
    for x, y in zip(ia, ib):
        xn, yn = x.isdigit(), y.isdigit()
        if xn and yn:
            c = _cmp(int(x), int(y))
        elif xn:
            c = -1
        elif yn:
            c = 1
        else:
            c = _cmp(x, y)
        if c:
            return c
    return _cmp(len(ia), len(ib))


def sort_versions(versions: list[str]) -> list[str]:
    return sorted(versions, key=functools.cmp_to_key(compare_versions))


def _run_tests() -> None:
    assert compare_versions("1.2.3", "1.2.3") == 0
    assert compare_versions("1.10.0", "1.9.0") == 1
    assert compare_versions("0.0.1", "0.1.0") == -1
    assert compare_versions("2.0.0", "1.99.99") == 1
    assert compare_versions("1.0.0-rc.1", "1.0.0") == -1
    assert compare_versions("1.0.0", "1.0.0-rc.1") == 1
    assert compare_versions("1.0.0-alpha", "1.0.0-alpha.1") == -1
    assert compare_versions("1.0.0-alpha.1", "1.0.0-alpha.beta") == -1
    assert compare_versions("1.0.0-beta.2", "1.0.0-beta.11") == -1
    assert compare_versions("1.0.0-rc.1", "1.0.0-beta.11") == 1
    for bad in ["", "1.0", "1.a.0", "1.0.0-", "v1.0.0"]:
        try:
            compare_versions(bad, "1.0.0")
            assert False, f"should reject {bad!r}"
        except ValueError:
            pass
    spec = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta",
            "1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0"]
    assert sort_versions(list(reversed(spec))) == spec
    print("All semver_compare tests passed.")


if __name__ == "__main__":
    _run_tests()
