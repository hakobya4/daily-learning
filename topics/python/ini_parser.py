"""
Day 15, Task 4 -- Python: tiny INI parser.

THE PROBLEM
------------
parse_ini(text) -> dict[str, dict[str, str]] for text like:

    ; a comment
    [server]
    host = example.com
    port=8080

Rules (keep it simple and exact):
  * Lines starting with ';' or '#' (after stripping) and blank lines are ignored.
  * "[name]" starts a section (strip spaces inside brackets).
  * "key = value" -> key and value each stripped; split on the FIRST '='.
  * Keys before any section go into section "" (empty string).
  * A repeated key in the same section: last one wins.
  * A non-blank, non-comment line with no '=' and not a section raises
    ValueError (message should contain the 1-based line number).
  * No inline-comment handling: "a = b ; c" has value "b ; c".

HOW TO WORK THROUGH THIS
-------------------------
Iterate with enumerate(text.splitlines(), 1), track the current section,
use setdefault to create sections lazily.

Run: python3 ini_parser.py
"""


def parse_ini(text: str) -> dict[str, dict[str, str]]:
    raise NotImplementedError


def _run_tests() -> None:
    text = "; c\n[server]\nhost = example.com\nport=8080\n\n# x\n[ db ]\nurl = a=b\n"
    assert parse_ini(text) == {
        "server": {"host": "example.com", "port": "8080"},
        "db": {"url": "a=b"},
    }
    assert parse_ini("k=v\n[s]\nk=1\nk=2") == {"": {"k": "v"}, "s": {"k": "2"}}
    assert parse_ini("") == {}
    assert parse_ini("[empty]") == {"empty": {}}
    assert parse_ini("a = b ; c") == {"": {"a": "b ; c"}}
    try:
        parse_ini("[s]\nok=1\noops\n")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "3" in str(e)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
