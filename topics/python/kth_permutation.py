"""
Day 21, Task 2 -- Python: k-th permutation sequence.

THE PROBLEM
------------
Return the k-th (1-indexed) permutation, in lexicographic order, of the
digits "1".."n" as a string. Do NOT generate all permutations.

  n = 3 -> "123","132","213","231","312","321"
  kth_permutation(3, 3) == "213"
  kth_permutation(4, 9) == "2314"

Raise ValueError if n < 1 or k is not in 1..n!.

HOW TO WORK THROUGH THIS
-------------------------
Use the factorial number system: with k0 = k - 1, the first digit is
index k0 // (n-1)! into the remaining sorted digits, then repeat with
k0 % (n-1)! on the rest.

Run: python3 kth_permutation.py
"""


def kth_permutation(n: int, k: int) -> str:
    raise NotImplementedError


def _run_tests():
    assert kth_permutation(1, 1) == "1"
    assert kth_permutation(3, 1) == "123"
    assert kth_permutation(3, 3) == "213"
    assert kth_permutation(3, 6) == "321"
    assert kth_permutation(4, 9) == "2314"
    assert kth_permutation(9, 362880) == "987654321"
    for n, k in [(0, 1), (3, 0), (3, 7)]:
        try:
            kth_permutation(n, k)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {(n, k)}")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
