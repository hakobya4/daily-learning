"""
Day 14, Task 10 -- Python: product of array except self (no division).

THE PROBLEM
------------
Given a list of ints `nums`, return a list `out` where out[i] is the
product of every element of nums EXCEPT nums[i]. You may NOT use
division, and it must run in O(n) time.

    [1, 2, 3, 4]  ->  [24, 12, 8, 6]
    [0, 2, 3]     ->  [6, 0, 0]
    [0, 0, 3]     ->  [0, 0, 0]

Edge cases: [] -> [], [5] -> [1].

Also implement product_except_self_extra_space_free(nums), the same
result but with O(1) EXTRA space beyond the output list (hint: fill the
output with prefix products, then sweep right-to-left with a running
suffix product).

HOW TO WORK THROUGH THIS
-------------------------
out[i] = (product of nums[:i]) * (product of nums[i+1:]). Compute
prefix products in one pass and suffix products in another.

Run: python3 product_except_self.py
"""


def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    prefix = [1] * n
    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]
    suffix = [1] * n
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]
    return [prefix[i] * suffix[i] for i in range(n)]


def product_except_self_extra_space_free(nums: list[int]) -> list[int]:
    n = len(nums)
    out = [1] * n
    for i in range(1, n):
        out[i] = out[i - 1] * nums[i - 1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]
    return out


def _run_tests() -> None:
    for fn in (product_except_self, product_except_self_extra_space_free):
        assert fn([]) == []
        assert fn([5]) == [1]
        assert fn([1, 2, 3, 4]) == [24, 12, 8, 6]
        assert fn([0, 2, 3]) == [6, 0, 0]
        assert fn([0, 0, 3]) == [0, 0, 0]
        assert fn([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
        import random
        random.seed(14)
        for _ in range(200):
            a = [random.randint(-4, 4) for _ in range(random.randint(0, 8))]
            want = []
            for i in range(len(a)):
                p = 1
                for j, v in enumerate(a):
                    if j != i:
                        p *= v
                want.append(p)
            assert fn(a) == want, a
    print("All product_except_self tests passed.")


if __name__ == "__main__":
    _run_tests()
