"""
Day 21, Task 3 -- Python: Gray code.

THE PROBLEM
------------
Return a list of the 2**n integers of an n-bit Gray code sequence:

  * it starts with 0 and contains every value 0..2**n - 1 exactly once
  * consecutive values differ in exactly one bit
  * the last and first values also differ in exactly one bit (cyclic)

  gray_code(0) == [0]
  gray_code(1) == [0, 1]
  gray_code(2) is e.g. [0, 1, 3, 2]

Any valid sequence is accepted by the tests. Raise ValueError if n < 0.

HOW TO WORK THROUGH THIS
-------------------------
The i-th Gray code is i ^ (i >> 1). Or build it by reflection: take the
(n-1)-bit list, then append its reverse with the top bit set.

Run: python3 gray_code.py
"""


def gray_code(n: int) -> list:
    raise NotImplementedError


def _one_bit(a: int, b: int) -> bool:
    x = a ^ b
    return x != 0 and x & (x - 1) == 0


def _run_tests():
    assert gray_code(0) == [0]
    assert gray_code(1) == [0, 1]
    for n in range(2, 8):
        seq = gray_code(n)
        assert len(seq) == 2 ** n
        assert seq[0] == 0
        assert sorted(seq) == list(range(2 ** n))
        for i in range(len(seq)):
            assert _one_bit(seq[i], seq[(i + 1) % len(seq)]), (n, i)
    try:
        gray_code(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
