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


_IDENT_CHARS = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-")
_WILDCARDS = ("x", "X", "*")


def _num(s):
    if not s or not s.isdigit() or not s.isascii():
        raise ValueError("invalid number %r" % (s,))
    if len(s) > 1 and s[0] == "0":
        raise ValueError("leading zero in %r" % (s,))
    return int(s)


def _parse_pre(s):
    idents = s.split(".")
    out = []
    for ident in idents:
        if not ident or any(c not in _IDENT_CHARS for c in ident):
            raise ValueError("invalid prerelease identifier %r" % (ident,))
        if ident.isdigit():
            out.append((0, _num(ident), ""))
        else:
            out.append((1, 0, ident))
    return tuple(out)


def _split_version(s):
    """Split off build and prerelease: returns (core, pre_tuple)."""
    if not isinstance(s, str):
        raise ValueError("version must be a string")
    if s.startswith("v"):
        s = s[1:]
    if "+" in s:
        s, build = s.split("+", 1)
        if not build or any(not p or any(c not in _IDENT_CHARS for c in p)
                            for p in build.split(".")):
            raise ValueError("invalid build metadata")
    pre = ()
    if "-" in s:
        s, pre_s = s.split("-", 1)
        pre = _parse_pre(pre_s)
    return s, pre


def _parse(s):
    core, pre = _split_version(s)
    parts = core.split(".")
    if len(parts) != 3:
        raise ValueError("not a full version: %r" % (s,))
    return (_num(parts[0]), _num(parts[1]), _num(parts[2]), pre)


def _cmp_pre(a, b):
    if a == b:
        return 0
    if not a:
        return 1   # no prerelease > with prerelease
    if not b:
        return -1
    for x, y in zip(a, b):
        if x != y:
            return -1 if x < y else 1
    return -1 if len(a) < len(b) else 1


def _cmp(va, vb):
    if va[:3] != vb[:3]:
        return -1 if va[:3] < vb[:3] else 1
    return _cmp_pre(va[3], vb[3])


def compare(a, b):
    return _cmp(_parse(a), _parse(b))


def _parse_partial(s):
    """Returns (nums, pre): nums is a list of 0-3 ints (missing/wildcard parts cut off)."""
    if s in ("",) + _WILDCARDS:
        return [], ()
    core, pre = _split_version(s)
    parts = core.split(".")
    if len(parts) > 3:
        raise ValueError("too many version parts: %r" % (s,))
    nums = []
    seen_wild = False
    for p in parts:
        if p in _WILDCARDS:
            seen_wild = True
        elif seen_wild:
            raise ValueError("number after wildcard in %r" % (s,))
        else:
            nums.append(_num(p))
    if pre and len(nums) != 3:
        raise ValueError("prerelease only allowed on a full version: %r" % (s,))
    return nums, pre


def _v(M, m=0, p=0, pre=()):
    return (M, m, p, pre)


def _xrange(nums, pre):
    if not nums:
        return []
    if len(nums) == 1:
        return [(">=", _v(nums[0])), ("<", _v(nums[0] + 1))]
    if len(nums) == 2:
        return [(">=", _v(nums[0], nums[1])), ("<", _v(nums[0], nums[1] + 1))]
    return [("=", _v(nums[0], nums[1], nums[2], pre))]


def _tilde(nums, pre):
    if len(nums) == 3:
        return [(">=", _v(nums[0], nums[1], nums[2], pre)), ("<", _v(nums[0], nums[1] + 1))]
    return _xrange(nums, pre)


def _caret(nums, pre):
    if not nums:
        return []
    M = nums[0]
    if len(nums) == 1:
        return [(">=", _v(M)), ("<", _v(M + 1))]
    m = nums[1]
    if len(nums) == 2:
        upper = _v(M + 1) if M > 0 else _v(0, m + 1)
        return [(">=", _v(M, m)), ("<", upper)]
    p = nums[2]
    if M > 0:
        upper = _v(M + 1)
    elif m > 0:
        upper = _v(0, m + 1)
    else:
        upper = _v(0, 0, p + 1)
    return [(">=", _v(M, m, p, pre)), ("<", upper)]


def _hyphen(lo, hi):
    lo_nums, lo_pre = _parse_partial(lo)
    hi_nums, hi_pre = _parse_partial(hi)
    out = []
    if lo_nums:
        filled = lo_nums + [0] * (3 - len(lo_nums))
        out.append((">=", _v(filled[0], filled[1], filled[2], lo_pre)))
    if len(hi_nums) == 3:
        out.append(("<=", _v(hi_nums[0], hi_nums[1], hi_nums[2], hi_pre)))
    elif len(hi_nums) == 2:
        out.append(("<", _v(hi_nums[0], hi_nums[1] + 1)))
    elif len(hi_nums) == 1:
        out.append(("<", _v(hi_nums[0] + 1)))
    return out


def _desugar(token):
    for op in (">=", "<=", ">", "<", "="):
        if token.startswith(op):
            return [(op, _parse(token[len(op):]))]
    if token.startswith("~"):
        return _tilde(*_parse_partial(token[1:]))
    if token.startswith("^"):
        return _caret(*_parse_partial(token[1:]))
    if token == "-":
        raise ValueError("misplaced hyphen")
    return _xrange(*_parse_partial(token))


def _holds(op, cmp_result):
    return {"=": cmp_result == 0, ">": cmp_result > 0, ">=": cmp_result >= 0,
            "<": cmp_result < 0, "<=": cmp_result <= 0}[op]


def satisfies(version, rng):
    v = _parse(version)
    if not isinstance(rng, str):
        raise ValueError("range must be a string")
    # Parse every alternative first so a malformed range always raises.
    alternatives = []
    for alt in rng.split("||"):
        tokens = alt.split()
        if len(tokens) == 3 and tokens[1] == "-":
            comps = _hyphen(tokens[0], tokens[2])
        else:
            comps = []
            for tok in tokens:
                comps.extend(_desugar(tok))
        alternatives.append(comps)
    for comps in alternatives:
        if not all(_holds(op, _cmp(v, cv)) for op, cv in comps):
            continue
        if v[3] and not any(cv[3] and cv[:3] == v[:3] for _, cv in comps):
            continue
        return True
    return False


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
