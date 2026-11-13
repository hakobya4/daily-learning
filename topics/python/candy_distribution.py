"""
Day 53, Task 1 -- Python: candy distribution (two-pass greedy).

THE PROBLEM
------------
min_candies(ratings): children stand in a line, each with a rating. Give every child at least
one candy, and any child with a strictly HIGHER rating than an immediate neighbour must get
MORE candies than that neighbour (equal ratings impose no constraint). Return the minimum
total number of candies (0 for an empty list).
Examples: [1, 0, 2] -> 5 (2, 1, 2), [1, 2, 2] -> 4 (1, 2, 1).
Hint: one left-to-right pass enforces the "left neighbour" rule, one right-to-left pass the
"right neighbour" rule; each child gets the max of the two. O(n) time. Bonus: O(1) space by
counting up/down slopes.

Run: python3 candy_distribution.py
"""


def min_candies(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


def _run_tests():
    assert min_candies([]) == 0
    assert min_candies([5]) == 1
    assert min_candies([1, 0, 2]) == 5
    assert min_candies([1, 2, 2]) == 4
    assert min_candies([1, 2, 3, 4]) == 10
    assert min_candies([4, 3, 2, 1]) == 10
    assert min_candies([1, 3, 2, 2, 1]) == 7
    assert min_candies([1, 2, 87, 87, 87, 2, 1]) == 13
    assert min_candies([3, 3, 3]) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
