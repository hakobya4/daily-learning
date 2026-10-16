"""
Day 26, Task 3 -- Python: longest repeating character replacement.

THE PROBLEM
------------
character_replacement(s, k) returns the length of the longest substring
that can be turned into all-the-same letter by replacing at most k
characters.

  character_replacement("ABAB", 2)    -> 4
  character_replacement("AABABBA", 1) -> 4

HOW TO WORK THROUGH THIS
-------------------------
Sliding window: keep counts of letters in the window. The window is valid
while (window length - count of the most frequent letter) <= k. Grow the
right edge, shrink the left edge when invalid. O(n).

Run: python3 longest_repeating_replacement.py
"""


def character_replacement(s: str, k: int) -> int:
    counts = {}
    left = 0
    max_freq = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        max_freq = max(max_freq, counts[ch])
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def _run_tests():
    assert character_replacement("ABAB", 2) == 4
    assert character_replacement("AABABBA", 1) == 4
    assert character_replacement("", 2) == 0
    assert character_replacement("AAAA", 0) == 4
    assert character_replacement("ABC", 0) == 1
    assert character_replacement("ABBB", 2) == 4
    assert character_replacement("ABCDE", 1) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
