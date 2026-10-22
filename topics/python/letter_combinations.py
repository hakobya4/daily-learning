"""
Day 32, Task 4 -- Python: letter combinations of a phone number.

THE PROBLEM
------------
Digits 2-9 map to letters like an old phone keypad:
  2 abc, 3 def, 4 ghi, 5 jkl, 6 mno, 7 pqrs, 8 tuv, 9 wxyz
letter_combinations(digits) returns every string the digit string could
spell, in lexicographic order (which is what you get by iterating the
digits left to right and the letters in keypad order). Empty input gives [].

  "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]
  "7"  -> ["p","q","r","s"]
  ""   -> []

HOW TO WORK THROUGH THIS
-------------------------
Backtracking: choose a letter for position i, recurse on i+1, and record
the path when i == len(digits). Or build iteratively by extending a list.

Run: python3 letter_combinations.py
"""

KEYPAD = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}


def letter_combinations(digits: str) -> list:
    raise NotImplementedError


def _run_tests():
    assert letter_combinations("") == []
    assert letter_combinations("7") == ["p", "q", "r", "s"]
    assert letter_combinations("23") == [
        "ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert len(letter_combinations("79")) == 16
    assert len(letter_combinations("234")) == 27
    r = letter_combinations("92")
    assert r[0] == "wa" and r[-1] == "zc" and r == sorted(r)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
