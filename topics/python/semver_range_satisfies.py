"""
Day 59, Task 10 -- Python: npm-style semver ranges (compare + satisfies).

THE PROBLEM
------------
Implement two functions.

compare(a, b) -> -1 | 0 | 1
    a and b are full SemVer 2.0.0 strings "MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]"
    (an optional leading "v" is allowed). Numbers have no leading zeros ("01" is
    invalid), PRERELEASE is dot-separated identifiers of [0-9A-Za-z-] (numeric
    identifiers also without leading zeros). BUILD metadata is ignored for ordering.
    Precedence (semver.org section 11):
      1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2
        < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
    i.e. a version WITHOUT prerelease is greater than the same version with one;
    identifiers compare left to right, numeric ones numerically and below any
    alphanumeric one, alphanumeric ones in ASCII order, and a shorter list wins a tie
    of equal prefixes as the SMALLER. Anything malformed raises ValueError.

satisfies(version, rng) -> bool
    rng is an npm-style range:
      * "||" separates alternatives (OR); inside one alternative, whitespace separates
        comparators that must ALL hold (AND).
      * comparators: ">", ">=", "<", "<=", "=" followed by a FULL version
        (">=1.2" is a ValueError in this exercise).
      * X-ranges: "*", "" (empty alternative), "x"/"X" -> any version;
        "1.x" / "1" -> >=1.0.0 <2.0.0;  "1.2.x" / "1.2" -> >=1.2.0 <1.3.0;
        a bare full version "1.2.3" means =1.2.3. A number after a wildcard
        ("1.x.3") is a ValueError.
      * tilde: ~1.2.3 -> >=1.2.3 <1.3.0;  ~1.2 -> >=1.2.0 <1.3.0;  ~1 -> >=1.0.0 <2.0.0
      * caret (don't change the left-most non-zero part):
          ^1.2.3 -> >=1.2.3 <2.0.0     ^0.2.3 -> >=0.2.3 <0.3.0    ^0.0.3 -> >=0.0.3 <0.0.4
          ^1.2.x -> >=1.2.0 <2.0.0     ^0.0.x / ^0.0 -> >=0.0.0 <0.1.0
          ^0.x / ^0 -> >=0.0.0 <1.0.0
      * hyphen: "A - B" (spaces around "-", exactly 3 tokens in that alternative)
          -> >=A' <=B, where a partial A is filled with zeros, and a partial B becomes
          an exclusive bound: "1.2.3 - 2.3" -> >=1.2.3 <2.4.0, "1.2.3 - 2" -> <3.0.0.
      * ~ and ^ (and the left side of a hyphen range) may carry a prerelease on a
        full version: ^1.2.4-alpha -> >=1.2.4-alpha <2.0.0.
    PRERELEASE RULE (npm): a version WITH a prerelease tag satisfies an alternative only
    if, besides all comparators holding, at least one comparator in THAT alternative has
    a prerelease tag on the very same MAJOR.MINOR.PATCH. So 1.2.4-beta.1 does NOT
    satisfy ">=1.2.3" but does satisfy ">=1.2.4-alpha", and 2.0.0-beta does not
    satisfy "^1.2.0". The synthetic upper bounds above carry no prerelease.
    Malformed version or range -> ValueError.

Hint: parse a version into (major, minor, patch, prerelease_tuple). Desugar every
token of an alternative into a list of plain (op, version) comparators first, then
evaluating is just compare() calls plus the prerelease check.

Run: python3 semver_range_satisfies.py
"""


def compare(a, b):
    raise NotImplementedError


def satisfies(version, rng):
    raise NotImplementedError


def _run_tests():
    order = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta",
             "1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0", "1.0.1",
             "1.1.0", "1.10.0", "2.0.0"]
    for i, x in enumerate(order):
        for j, y in enumerate(order):
            expected = (i > j) - (i < j)
            assert compare(x, y) == expected, (x, y)
    assert compare("1.0.0+build.1", "1.0.0+build.2") == 0
    assert compare("v1.2.3", "1.2.3") == 0
    for bad in ["1.2", "01.2.3", "1.02.3", "1.2.3-01", "a.b.c", "1.2.3.4", "1.2.3-", ""]:
        try:
            compare(bad, "1.0.0")
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)

    cases = [
        ("1.2.3", "^1.2.0", True), ("2.0.0", "^1.2.0", False),
        ("1.9.9", "~1.2.0", False), ("1.2.9", "~1.2.0", True),
        ("0.2.5", "^0.2.3", True), ("0.3.0", "^0.2.3", False),
        ("0.0.3", "^0.0.3", True), ("0.0.4", "^0.0.3", False),
        ("0.0.9", "^0.0.x", True), ("0.1.9", "^0.0.x", False),
        ("0.9.9", "^0.x", True), ("1.0.0", "^0.x", False),
        ("1.9.0", "^1.2.x", True), ("1.1.9", "^1.2.x", False),
        ("1.5.0", "1.2.3 - 1.5", True), ("1.6.0", "1.2.3 - 1.5", False),
        ("2.9.9", "1.2.3 - 2", True), ("3.0.0", "1.2.3 - 2", False),
        ("2.3.4", "1.2 - 2.3.4", True), ("1.0.0", "1.2 - 2.3.4", False),
        ("1.2.0", "1.2 - 2.3.4", True),
        ("3.0.0", "<2.0.0 || >=3.0.0", True), ("2.5.0", "<2.0.0 || >=3.0.0", False),
        ("1.4.0", ">1.2.3 <1.5.0", True), ("1.5.0", ">1.2.3 <1.5.0", False),
        ("1.2.3", ">1.2.3 <1.5.0", False), ("1.2.3", "<=1.2.3", True),
        ("5.0.0", "*", True), ("5.0.0", "", True), ("5.0.0", "x", True),
        ("1.2.0", "1.2.x", True), ("1.3.0", "1.2", False), ("1.0.7", "1", True),
        ("1.2.3", "1.2.3", True), ("1.2.4", "1.2.3", False),
        ("1.0.0+build.5", "=1.0.0", True), ("v1.0.0", "1.x || 3.x", True),
        ("2.0.0", "1.x || 3.x", False),
        # prerelease rule
        ("1.2.4-beta.1", ">=1.2.3", False), ("1.2.4-beta.1", ">=1.2.4-alpha", True),
        ("1.2.4-alpha", ">=1.2.4-alpha.1", False), ("1.3.0-rc.1", "^1.2.4-alpha", False),
        ("1.2.5", "^1.2.4-alpha", True), ("2.0.0-beta", "^1.2.0", False),
        ("1.0.0-alpha", "1.0.0-alpha", True), ("1.0.0", ">1.0.0-rc.1 <1.0.1", True),
        ("1.0.0-rc.2", ">1.0.0-rc.1 <1.0.1", True),
        ("1.0.0-rc.1", "1.0.0-rc.1 - 1.0.0", True), ("1.0.0-rc.2", "~1.0.0-rc.1", True),
        ("1.0.1-rc.1", "~1.0.0-rc.1", False),
        ("1.0.1-rc.1", "~1.0.0-rc.1 || >=1.0.1-alpha", True),
        ("1.0.0-beta", "*", False),
    ]
    for v, r, exp in cases:
        assert satisfies(v, r) is exp, (v, r, exp)

    for bad_v, bad_r in [("1.2", "*"), ("1.0.0", ">=1.2"), ("1.0.0", "^x.1"),
                         ("1.0.0", "1.2.3 - "), ("1.0.0", "1 - 2 - 3"), ("1.0.0", "~1.x.3"),
                         ("1.0.0", ">=foo"), ("1.0.0", "1.x.3")]:
        try:
            satisfies(bad_v, bad_r)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r %r" % (bad_v, bad_r))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
