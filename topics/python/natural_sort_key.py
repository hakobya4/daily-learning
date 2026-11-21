"""
Day 61, Task 2 -- Python: "natural" (human) sort order for file names and versions.

THE PROBLEM
------------
sorted(["file10.txt", "file2.txt", "file1.txt"]) gives file1, file10, file2 because
strings compare character by character. File managers show file1, file2, file10.

1) tokenize(s) -> list
   Split s into maximal runs of ASCII digits and maximal runs of non-digits, in order.
   Digit runs become ints, other runs stay strings:
     tokenize("img12b007.png") -> ["img", 12, "b", 7, ".png"]
     tokenize("42")            -> [42]
     tokenize("")              -> []
   Only "0".."9" count as digits (str.isdigit() also accepts "²" etc. -- don't use it).

2) natural_key(s) -> a value usable as sorted(..., key=natural_key) with these rules:
   a) compare the token sequences left to right;
   b) a number token sorts BEFORE a text token at the same position
      ("1abc" < "abc");
   c) numbers compare by numeric value; text compares CASE-INSENSITIVELY
      (casefold) -- "Apple" and "apple" are equal at this stage;
   d) if one token sequence is a prefix of the other, the shorter sorts first
      ("file" < "file1" < "file1a");
   e) TIE-BREAKS when everything above is equal (in this order):
        - fewer leading zeros first, comparing number tokens left to right
          ("a1" < "a01" < "a001");
        - then plain string comparison of the original s (so "Apple" < "apple",
          because "A" < "a"), which makes the order total and deterministic.
   Hint: build a tuple of (kind, value) pairs, e.g. (0, n) for numbers and (1, text)
   for text -- tuples compare element-wise and a shorter tuple that is a prefix sorts
   first. Then append the tie-break parts as extra trailing elements (careful: rule d
   must still win over the tie-breaks, so wrap the main part in its own tuple).

3) natural_sorted(items, reverse=False) -> list   (just sorted() with your key)

Run: python3 natural_sort_key.py
"""


def _runs(s):
    """Yield (is_digit_run, text) for maximal runs of ASCII digits / non-digits."""
    i, n = 0, len(s)
    while i < n:
        isd = "0" <= s[i] <= "9"
        j = i + 1
        while j < n and ("0" <= s[j] <= "9") == isd:
            j += 1
        yield isd, s[i:j]
        i = j


def tokenize(s):
    return [int(run) if isd else run for isd, run in _runs(s)]


def natural_key(s):
    main = []
    zeros = []
    for isd, run in _runs(s):
        if isd:
            value = int(run)
            main.append((0, value))
            zeros.append(len(run) - len(str(value)))
        else:
            main.append((1, run.casefold()))
    return (tuple(main), tuple(zeros), s)


def natural_sorted(items, reverse=False):
    return sorted(items, key=natural_key, reverse=reverse)


def _run_tests():
    assert tokenize("img12b007.png") == ["img", 12, "b", 7, ".png"]
    assert tokenize("42") == [42]
    assert tokenize("") == []
    assert tokenize("abc") == ["abc"]
    assert tokenize("v1.10.3") == ["v", 1, ".", 10, ".", 3]
    assert tokenize("x²y") == ["x²y"]          # superscript two is not a digit
    assert tokenize("007") == [7]

    assert natural_sorted(["file10.txt", "file2.txt", "file1.txt"]) == \
        ["file1.txt", "file2.txt", "file10.txt"]
    assert natural_sorted(["abc", "1abc", "10", "9"]) == ["1abc", "9", "10", "abc"]
    assert natural_sorted(["file1a", "file", "file1"]) == ["file", "file1", "file1a"]
    assert natural_sorted(["a001", "a01", "a1", "a2"]) == ["a1", "a01", "a001", "a2"]
    assert natural_sorted(["apple", "Banana", "Apple", "banana"]) == \
        ["Apple", "apple", "Banana", "banana"]
    assert natural_sorted(["v1.10.0", "v1.9.2", "v1.9.10", "v1.9.9", "V1.2"]) == \
        ["V1.2", "v1.9.2", "v1.9.9", "v1.9.10", "v1.10.0"]
    assert natural_sorted(["x10y2", "x10y10", "x9y99", "x10"]) == \
        ["x9y99", "x10", "x10y2", "x10y10"]
    assert natural_sorted(["b", "a", "c"], reverse=True) == ["c", "b", "a"]
    assert natural_sorted(["Chapter 2", "chapter 10", "Chapter 1"]) == \
        ["Chapter 1", "Chapter 2", "chapter 10"]
    assert natural_sorted(["", "0", "a"]) == ["", "0", "a"]
    assert natural_sorted(["2024-1-15", "2024-01-5", "2024-1-5"]) == \
        ["2024-1-5", "2024-01-5", "2024-1-15"]
    big = "n" + "9" * 40
    assert natural_sorted([big, "n10"]) == ["n10", big]

    # determinism: the key gives a total order -- any input permutation sorts the same
    import random
    rng = random.Random(61)
    words = ["a1", "A1", "a01", "a1b", "a", "A", "b2", "b10", "B02", "10", "1", "01", "",
             "x.5", "x.05", "x.50", "img007", "img7", "IMG7"]
    first = natural_sorted(words)
    for _ in range(50):
        w = words[:]
        rng.shuffle(w)
        assert natural_sorted(w) == first
    assert len(set(map(natural_key, words))) == len(words)  # no two keys equal
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
