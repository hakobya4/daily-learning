"""
Day 16, Task 4 -- Python: full text justification.

THE PROBLEM
------------
justify(words, width) packs words greedily into lines of exactly `width`
characters. Extra spaces are distributed as evenly as possible between
words, extra ones going to the LEFT gaps. The last line, and any line
with a single word, is left-justified (single spaces, padded right).

    justify(["This","is","an","example","of","text","justification."], 16)
      -> ["This    is    an",
          "example  of text",
          "justification.  "]

    justify(["a"], 3) -> ["a  "]

Assume every word is 1..width characters long. Return [] for no words.

HOW TO WORK THROUGH THIS
-------------------------
Greedy: collect words while len(words)+gaps fits. divmod(spaces, gaps)
gives the base spacing and how many left gaps get one extra space.

Run: python3 text_justify.py
"""


def justify(words: list[str], width: int) -> list[str]:
    raise NotImplementedError


def _run_tests():
    out = justify(["This", "is", "an", "example", "of", "text", "justification."], 16)
    assert out == ["This    is    an", "example  of text", "justification.  "], out
    assert justify(["a"], 3) == ["a  "]
    assert justify([], 5) == []
    out = justify(["What", "must", "be", "acknowledgment", "shall", "be"], 16)
    assert out == ["What   must   be", "acknowledgment  ", "shall be        "], out
    out = justify(["Listen", "to", "many,", "speak", "to", "a", "few."], 6)
    assert out == ["Listen", "to    ", "many, ", "speak ", "to   a", "few.  "], out
    assert all(len(line) == 6 for line in out)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
