"""
Day 42, Task 1 -- Python: camelCase <-> snake_case conversion.

THE PROBLEM
------------
to_snake(s) -> convert camelCase / PascalCase to snake_case.
  "camelCase" -> "camel_case", "HTTPServer" -> "http_server",
  "parseXMLFile" -> "parse_xml_file", "already_snake" stays unchanged.
  Runs of capitals are one word, split before the last capital when a
  lowercase letter follows ("XMLFile" -> "xml_file"). Digits stay glued to
  the preceding word ("utf8Encode" -> "utf8_encode").
to_camel(s) -> inverse for snake_case: "parse_xml_file" -> "parseXmlFile".
  Leading/trailing/double underscores are dropped. Empty -> empty.

Run: python3 camel_snake.py
"""


def to_snake(s: str) -> str:
    out = []
    for i, ch in enumerate(s):
        if ch.isupper() and i > 0:
            prev = s[i - 1]
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if prev.islower() or prev.isdigit() or (prev.isupper() and nxt.islower()):
                out.append("_")
        out.append(ch.lower())
    return "".join(out)


def to_camel(s: str) -> str:
    parts = [p for p in s.split("_") if p]
    if not parts:
        return ""
    return parts[0] + "".join(p[0].upper() + p[1:] for p in parts[1:])


def _run_tests():
    assert to_snake("camelCase") == "camel_case"
    assert to_snake("PascalCase") == "pascal_case"
    assert to_snake("HTTPServer") == "http_server"
    assert to_snake("parseXMLFile") == "parse_xml_file"
    assert to_snake("already_snake") == "already_snake"
    assert to_snake("utf8Encode") == "utf8_encode"
    assert to_snake("") == ""
    assert to_snake("a") == "a"
    assert to_camel("parse_xml_file") == "parseXmlFile"
    assert to_camel("x") == "x"
    assert to_camel("__private_name_") == "privateName"
    assert to_camel("a__b") == "aB"
    assert to_camel("") == ""
    for s in ["fooBar", "a", "someLongVariableName"]:
        assert to_camel(to_snake(s)) == s
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
