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


def compare_versions(a: str, b: str) -> int:
    raise NotImplementedError


def sort_versions(versions: list[str]) -> list[str]:
    raise NotImplementedError


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
