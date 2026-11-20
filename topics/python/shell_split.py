"""
Day 60, Task 2 -- Python: POSIX shell-style word splitting and quoting (a mini shlex).

THE PROBLEM
------------
Implement, WITHOUT importing shlex (or re):

1) shell_split(s) -> list[str]   -- must behave exactly like shlex.split(s) (posix=True,
   no comments) on every input. The rules:
     - whitespace (space, tab, \\r, \\n) separates words; runs of it are one separator;
     - '...'  single quotes: everything inside is literal, backslashes included;
     - "..."  double quotes: everything is literal EXCEPT a backslash followed by " or
              \\ (those two are escaped: \\" -> ", \\\\ -> \\); a backslash before any
              other character is kept as-is ("a\\$b" -> a\\$b);
     - outside quotes a backslash escapes ANY next character, whitespace and newline
       included ("a\\ b" -> one word "a b");
     - quoted and unquoted parts glue into one word as long as no unquoted whitespace
       separates them (a"b c"'d' -> "ab cd"), and '' or "" alone makes an EMPTY word;
     - an unclosed quote raises ValueError("No closing quotation"); a backslash as the
       very last character (outside single quotes) raises ValueError("No escaped character").

2) shell_quote(s) -> str   -- exactly like shlex.quote(s):
     - "" -> "''";
     - if every character is in A-Z a-z 0-9 and @%+=:,./-_ return s unchanged;
     - otherwise wrap in single quotes, turning each ' into '"'"'.
   So shell_split(" ".join(map(shell_quote, args))) == args for any list of strings.

Hint: a small state machine with states NONE / WORD / SQ / DQ / ESC and a flag that
records "a word has started" (needed so '' produces an empty word). Feed one character
at a time; at end of input, an open SQ/DQ is an error and an open WORD is emitted.

Run: python3 shell_split.py
"""


def shell_split(s):
    raise NotImplementedError


def shell_quote(s):
    raise NotImplementedError


def _run_tests():
    cases = [
        ("", []),
        ("   ", []),
        ("a b  c", ["a", "b", "c"]),
        ("  lead\ttab\nnl  ", ["lead", "tab", "nl"]),
        ("'a b' c", ["a b", "c"]),
        ('"a b" c', ["a b", "c"]),
        ("a\\ b", ["a b"]),
        ("a\"b c\"'d'", ["ab cd"]),
        ("''", [""]),
        ('"" x \'\'', ["", "x", ""]),
        ("'it\\'s'", None),  # the \\ is literal inside '...', so the last ' is unclosed
        ("'it\\'s", ["it\\s"]),
        ("'a\\b'", ["a\\b"]),
        ('"a\\"b"', ['a"b']),
        ('"a\\\\b"', ["a\\b"]),
        ('"a\\$b"', ["a\\$b"]),
        ('"a\\nb"', ["a\\nb"]),
        ("a\\\nb", ["a\nb"]),
        ("echo \"it's\" 'say \"hi\"'", ["echo", "it's", 'say "hi"']),
        ('grep -E "^(foo|bar)$" file.txt', ["grep", "-E", "^(foo|bar)$", "file.txt"]),
        ("x#y #z", ["x#y", "#z"]),
    ]
    for s, exp in cases:
        if exp is None:
            try:
                shell_split(s)
            except ValueError:
                continue
            raise AssertionError("expected ValueError for %r" % s)
        assert shell_split(s) == exp, (s, shell_split(s), exp)
    for bad, msg in [("'abc", "No closing quotation"), ('"abc', "No closing quotation"),
                     ("abc\\", "No escaped character"), ('"ab\\', "No escaped character")]:
        try:
            shell_split(bad)
        except ValueError as e:
            assert str(e) == msg, (bad, str(e))
        else:
            raise AssertionError("expected ValueError for %r" % bad)

    # randomized comparison against the real shlex (allowed in the TESTS only)
    import random
    import shlex
    rng = random.Random(60)
    alphabet = "ab '\"\\\t\n$#"
    for _ in range(4000):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
        try:
            want = shlex.split(s)
        except ValueError as e:
            want = ("error", str(e))
        try:
            got = shell_split(s)
        except ValueError as e:
            got = ("error", str(e))
        assert got == want, (s, got, want)

    for s in ["", "abc", "a b", "it's", "$HOME", "a\"b", "-rf", "x=1,y=2", "tab\there",
              "@%+=:,./-_", "naïve", "*.py", "'"]:
        assert shell_quote(s) == shlex.quote(s), (s, shell_quote(s))
    for _ in range(2000):
        args = ["".join(rng.choice(alphabet + "xyz") for _ in range(rng.randint(0, 6)))
                for _ in range(rng.randint(0, 4))]
        assert shell_split(" ".join(map(shell_quote, args))) == args, args
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
