"""
Day 35, Task 10 -- CS fundamentals: Sieve of Eratosthenes.

THE PROBLEM
------------
Implement two functions:

  primes_below(n)  -> sorted list of all primes strictly less than n
  count_primes(n)  -> how many primes are strictly less than n

Use the sieve (a boolean array, crossing off multiples), NOT trial division
per number: count_primes(5_000_000) must finish in a couple of seconds.

  primes_below(10) -> [2, 3, 5, 7]
  count_primes(100) -> 25

HOW TO WORK THROUGH THIS
-------------------------
is_prime = [True] * n; mark 0 and 1 False. For p from 2 while p*p < n: if
is_prime[p], cross off p*p, p*p+p, ... Remember n <= 2 has no primes.

Run: python3 count_primes_sieve.py
"""


def _sieve(n: int) -> bytearray:
    is_prime = bytearray([1]) * max(n, 0)
    for i in range(min(2, len(is_prime))):
        is_prime[i] = 0
    p = 2
    while p * p < n:
        if is_prime[p]:
            is_prime[p * p::p] = bytearray(len(range(p * p, n, p)))
        p += 1
    return is_prime


def primes_below(n: int) -> list:
    return [i for i, v in enumerate(_sieve(n)) if v]


def count_primes(n: int) -> int:
    return sum(_sieve(n))


def _run_tests():
    assert primes_below(0) == []
    assert primes_below(2) == []
    assert primes_below(3) == [2]
    assert primes_below(10) == [2, 3, 5, 7]
    assert primes_below(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert count_primes(100) == 25
    assert count_primes(1000) == 168
    assert count_primes(1_000_000) == 78498
    assert count_primes(5_000_000) == 348513
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
