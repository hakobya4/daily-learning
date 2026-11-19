"""
Day 59, Task 1 -- Python: a path-aware glob matcher with ** (gitignore/pathlib style).

THE PROBLEM
------------
Implement match(pattern, path) -> bool WITHOUT using fnmatch, glob, pathlib.match or re.

Both pattern and path are split on "/" into segments; a pattern segment matches one
path segment, except for the special segment "**":
  *        any run of characters (possibly empty) inside ONE segment (never "/")
  ?        exactly one character (never "/")
  [abc]    one character from the set; ranges like [a-z0-9]; [!...] negates.
           A "]" right after "[" or "[!" is a literal member ("[]]", "[!]]"); a "-"
           first or last is literal ("[a-]"). An unclosed "[" or a reversed range
           ("[z-a]") raises ValueError.
  \\x      the character x literally (so "\\*" is a real asterisk); a trailing lone
           backslash raises ValueError.
  **       when it is a WHOLE segment: zero or more whole path segments
           ("src/**" matches "src" and "src/a/b"; "**/*.py" matches "main.py").
           Inside a segment ("a**b") it is just "*".
Hidden files: a path segment that starts with "." is only matched by a pattern segment
that starts with a LITERAL "." (so "*" does not match ".hidden" but ".*" does).
"**" as a whole segment is the exception: it does cross dot-directories.
Matching is case-sensitive and must match the WHOLE path.

Examples:
  match("src/**/test_*.py", "src/a/b/test_x.py") -> True
  match("*.py", "src/main.py")                   -> False  (* never crosses "/")
  match("a/**/b/**/c", "a/x/c")                  -> False
  match("file[0-9][0-9].log", "file07.log")      -> True

Hint: two levels. First tokenize each pattern segment (literal / star / any / class),
then match tokens against one segment with memoised recursion on (token_idx, char_idx)
-- a star tries every split. Then do the same one level up on (pattern_seg_idx,
path_seg_idx), where "**" tries every number of skipped segments. Memoisation keeps
patterns like "a*a*a*a*b" vs "aaaaaaaaaaaaaaaaaaaa" fast.

Run: python3 glob_match.py
"""


def _tokenize(seg):
    """Turn one pattern segment into tokens: ('lit', c), ('star',), ('any',), ('cls', neg, items)."""
    toks = []
    i, n = 0, len(seg)
    while i < n:
        c = seg[i]
        if c == "\\":
            if i + 1 >= n:
                raise ValueError("trailing backslash in pattern")
            toks.append(("lit", seg[i + 1]))
            i += 2
        elif c == "*":
            if not (toks and toks[-1][0] == "star"):
                toks.append(("star",))
            i += 1
        elif c == "?":
            toks.append(("any",))
            i += 1
        elif c == "[":
            j = i + 1
            neg = False
            if j < n and seg[j] == "!":
                neg = True
                j += 1
            members = []
            first = True
            while True:
                if j >= n:
                    raise ValueError("unclosed '[' in pattern")
                ch = seg[j]
                if ch == "]" and not first:
                    break
                first = False
                if ch == "\\" and j + 1 < n:
                    ch = seg[j + 1]
                    j += 1
                # range?
                if j + 2 < n and seg[j + 1] == "-" and seg[j + 2] != "]":
                    hi = seg[j + 2]
                    if hi == "\\" and j + 3 < n:
                        hi = seg[j + 3]
                        j += 1
                    if ord(hi) < ord(ch):
                        raise ValueError("reversed range in pattern")
                    members.append((ch, hi))
                    j += 3
                else:
                    members.append((ch, ch))
                    j += 1
            toks.append(("cls", neg, tuple(members)))
            i = j + 1
        else:
            toks.append(("lit", c))
            i += 1
    return toks


def _match_segment(toks, s):
    # Hidden-file rule: a segment starting with "." needs a literal "." first token.
    if s.startswith(".") and not (toks and toks[0] == ("lit", ".")):
        return False
    memo = {}
    nt, ns = len(toks), len(s)

    def go(ti, si):
        key = (ti, si)
        if key in memo:
            return memo[key]
        if ti == nt:
            res = si == ns
        else:
            t = toks[ti]
            kind = t[0]
            if kind == "star":
                res = any(go(ti + 1, k) for k in range(si, ns + 1))
            elif si == ns:
                res = False
            elif kind == "lit":
                res = s[si] == t[1] and go(ti + 1, si + 1)
            elif kind == "any":
                res = go(ti + 1, si + 1)
            else:
                ch = s[si]
                inside = any(lo <= ch <= hi for lo, hi in t[2])
                res = (inside != t[1]) and go(ti + 1, si + 1)
        memo[key] = res
        return res

    return go(0, 0)


def match(pattern, path):
    psegs = pattern.split("/")
    # Tokenize every segment up front so malformed patterns always raise.
    ptoks = [None if seg == "**" else _tokenize(seg) for seg in psegs]
    segs = path.split("/")
    np_, ns = len(ptoks), len(segs)
    memo = {}

    def go(pi, si):
        key = (pi, si)
        if key in memo:
            return memo[key]
        if pi == np_:
            res = si == ns
        elif ptoks[pi] is None:  # "**": zero or more whole segments
            res = any(go(pi + 1, k) for k in range(si, ns + 1))
        elif si == ns:
            res = False
        else:
            res = _match_segment(ptoks[pi], segs[si]) and go(pi + 1, si + 1)
        memo[key] = res
        return res

    return go(0, 0)


def _run_tests():
    cases = [
        ("*.py", "main.py", True), ("*.py", "src/main.py", False),
        ("src/*.py", "src/main.py", True), ("**/*.py", "main.py", True),
        ("**/*.py", "a/b/c.py", True), ("src/**", "src", True),
        ("src/**", "src/a/b", True), ("src/**/test_*.py", "src/test_x.py", True),
        ("src/**/test_*.py", "src/a/b/test_x.py", True), ("a/**/b/**/c", "a/b/c", True),
        ("a/**/b/**/c", "a/x/b/y/z/c", True), ("a/**/b/**/c", "a/x/c", False),
        ("?.txt", "a.txt", True), ("?.txt", "ab.txt", False),
        ("[abc].md", "b.md", True), ("[!abc].md", "b.md", False),
        ("[!abc].md", "d.md", True), ("file[0-9][0-9].log", "file07.log", True),
        ("file[0-9][0-9].log", "file7.log", False), ("[]]x", "]x", True),
        ("[!]]x", "ax", True), ("[!]]x", "]x", False), ("[a-]x", "-x", True),
        ("\\*.txt", "*.txt", True), ("\\*.txt", "a.txt", False),
        ("*", ".hidden", False), (".*", ".hidden", True), ("?hidden", ".hidden", False),
        ("[.]hidden", ".hidden", False), ("**/*.cfg", ".git/x.cfg", True),
        ("*/x.cfg", ".git/x.cfg", False), ("*.py", "a/.py", False),
        ("a*b*c", "abc", True), ("a*b*c", "axxbyyc", True), ("a*b*c", "acb", False),
        ("a**b", "axyb", True), ("a**b", "ax/yb", False), ("**", "a/b/c", True),
        ("*/*", "a/b", True), ("*/*", "a/b/c", False), ("Main.py", "main.py", False),
        ("a?c", "a/c", False), ("**/b", "b", True), ("x/**/y", "x/y/y/y", True),
    ]
    for p, s, exp in cases:
        assert match(p, s) is exp, (p, s, exp)
    assert match("a*a*a*a*a*a*b", "a" * 40) is False
    assert match("**/**/**/**/z", "/".join("q" * 30) + "/y") is False
    for bad in ["[abc", "x[!", "[z-a]", "abc\\"]:
        try:
            match(bad, "abc")
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
