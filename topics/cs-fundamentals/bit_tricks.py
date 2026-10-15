"""
Day 24, Task 9 -- CS fundamentals: bit manipulation toolkit.

THE PROBLEM
------------
Implement four functions WITHOUT using bin(), str formatting, int.bit_count()
or loops over string digits (use bit operators):

  count_set_bits(n)      number of 1 bits in a non-negative int
  is_power_of_two(n)     True iff n > 0 and exactly one bit is set
  single_number(nums)    every value appears twice except one; return it (XOR)
  reverse_bits32(n)      reverse the 32 bits of an unsigned 32-bit int

  count_set_bits(0b10110) == 3
  is_power_of_two(64) is True, is_power_of_two(0) is False
  single_number([4, 1, 2, 1, 2]) == 4
  reverse_bits32(1) == 2**31

Raise ValueError for a negative n in count_set_bits, and for n outside
0 <= n < 2**32 in reverse_bits32.

HOW TO WORK THROUGH THIS
-------------------------
Kernighan: n &= n - 1 clears the lowest set bit. A power of two satisfies
n & (n - 1) == 0. x ^ x == 0 and x ^ 0 == x. For reversal, shift the result
left and OR in (n & 1), 32 times.

Run: python3 bit_tricks.py
"""


def count_set_bits(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def single_number(nums: list) -> int:
    result = 0
    for x in nums:
        result ^= x
    return result


def reverse_bits32(n: int) -> int:
    if n < 0 or n >= 2**32:
        raise ValueError("n must satisfy 0 <= n < 2**32")
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def _run_tests():
    assert count_set_bits(0) == 0
    assert count_set_bits(0b10110) == 3
    assert count_set_bits(2**40 - 1) == 40
    for n in range(0, 300):
        assert count_set_bits(n) == bin(n).count("1")
    assert is_power_of_two(1) is True
    assert is_power_of_two(64) is True
    assert is_power_of_two(0) is False
    assert is_power_of_two(-8) is False
    assert is_power_of_two(12) is False
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([7]) == 7
    assert single_number([-3, 5, 5]) == -3
    assert reverse_bits32(1) == 2**31
    assert reverse_bits32(0) == 0
    assert reverse_bits32(0b00000010100101000001111010011100) == 964176192
    assert reverse_bits32(2**32 - 1) == 2**32 - 1
    for n in (0, 12345, 2**31, 987654321):
        assert reverse_bits32(reverse_bits32(n)) == n
    for fn, bad in ((count_set_bits, -1), (reverse_bits32, -1), (reverse_bits32, 2**32)):
        try:
            fn(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
