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


def match(pattern, path):
    raise NotImplementedError


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
