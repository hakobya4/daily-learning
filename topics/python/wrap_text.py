"""
Day 11, Task 3 -- Python: greedy word wrap.

THE PROBLEM
------------
Write wrap_text(text: str, width: int) -> list[str] that splits text
into lines of at most `width` characters, breaking only at whitespace.

Rules:
  - Words are separated by any run of whitespace; output lines join
    words with exactly one space and have no leading/trailing spaces.
  - Greedy: put as many words on a line as fit.
  - A single word longer than width is hard-split into width-sized
    chunks (the last chunk may be shorter and may be followed by more
    words on the same line if they fit).
  - Empty / whitespace-only text returns [].
  - Raise ValueError if width < 1.

HOW TO WORK THROUGH THIS
-------------------------
Keep a current-line list and its length. For each word, if it does not
fit, flush the line first. Handle the over-long word before placing it.

Run: python3 wrap_text.py
"""


def wrap_text(text: str, width: int) -> list[str]:
    if width < 1:
        raise ValueError("width must be >= 1")
    lines = []
    cur = []
    cur_len = 0
    for word in text.split():
        while len(word) > width:
            # hard-split: flush the current line, emit full chunks
            if cur:
                lines.append(" ".join(cur))
                cur, cur_len = [], 0
            lines.append(word[:width])
            word = word[width:]
        if not cur:
            cur, cur_len = [word], len(word)
        elif cur_len + 1 + len(word) <= width:
            cur.append(word)
            cur_len += 1 + len(word)
        else:
            lines.append(" ".join(cur))
            cur, cur_len = [word], len(word)
    if cur:
        lines.append(" ".join(cur))
    return lines


def _run_tests() -> None:
    assert wrap_text("", 10) == []
    assert wrap_text("   \n\t ", 10) == []
    assert wrap_text("the quick brown fox", 10) == ["the quick", "brown fox"]
    assert wrap_text("the quick brown fox", 20) == ["the quick brown fox"]
    assert wrap_text("a  b\n\nc", 3) == ["a b", "c"]
    assert wrap_text("aaa bbb ccc", 3) == ["aaa", "bbb", "ccc"]
    assert wrap_text("abcdefgh", 3) == ["abc", "def", "gh"]
    assert wrap_text("abcde x", 3) == ["abc", "de", "x"]
    assert wrap_text("abcde x", 4) == ["abcd", "e x"]
    for line in wrap_text("lorem ipsum dolor sit amet consectetur", 12):
        assert 0 < len(line) <= 12
    try:
        wrap_text("x", 0)
        assert False, "should reject width 0"
    except ValueError:
        pass
    print("All wrap_text tests passed.")


if __name__ == "__main__":
    _run_tests()
