"""
Day 40, Task 2 -- Python: fast exponentiation.

THE PROBLEM
------------
Implement my_pow(x, n) for float x and integer n (possibly negative or zero)
WITHOUT using ** or math.pow. Use exponentiation by squaring so it runs in
O(log |n|) multiplications. my_pow(x, 0) == 1.0 for any x.

  my_pow(2.0, 10)  -> 1024.0
  my_pow(2.0, -2)  -> 0.25

Also implement pow_mod(base, exp, mod) -> (base ** exp) % mod for exp >= 0
without ever building the huge number (square and reduce each step).

HOW TO WORK THROUGH THIS
-------------------------
Loop over the bits of n: if the low bit is 1 multiply result by the current
square; then square the base and shift n right. For negative n, compute with
|n| and take the reciprocal at the end.

Run: python3 fast_power.py
"""


def my_pow(x: float, n: int) -> float:
    raise NotImplementedError


def pow_mod(base: int, exp: int, mod: int) -> int:
    raise NotImplementedError


def _run_tests():
    assert my_pow(2.0, 10) == 1024.0
    assert my_pow(2.0, -2) == 0.25
    assert my_pow(5.0, 0) == 1.0
    assert my_pow(0.0, 0) == 1.0
    assert my_pow(1.0, 10**9) == 1.0
    assert my_pow(-1.0, 10**9 + 1) == -1.0
    assert abs(my_pow(2.1, 3) - 9.261) < 1e-9
    assert abs(my_pow(10.0, -3) - 0.001) < 1e-12
    assert pow_mod(2, 10, 1000) == 24
    assert pow_mod(3, 0, 7) == 1
    assert pow_mod(7, 128, 13) == pow(7, 128, 13)
    assert pow_mod(123456789, 10**18, 10**9 + 7) == pow(123456789, 10**18, 10**9 + 7)
    assert pow_mod(5, 3, 1) == 0
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
