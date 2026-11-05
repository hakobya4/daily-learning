"""
Day 46, Task 9 -- CS fundamentals: matrix chain multiplication (interval DP).

THE PROBLEM
------------
dims has n+1 entries: matrix i (0-based) has shape dims[i] x dims[i+1].
matrix_chain_cost(dims) returns the minimum number of scalar multiplications
needed to multiply all n matrices (multiplying p x q by q x r costs p*q*r).
With 0 or 1 matrices the cost is 0.
Hint: dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1],
filled by increasing chain length. O(n^3).

Run: python3 matrix_chain_order.py
"""


def matrix_chain_cost(dims):
    raise NotImplementedError


def _run_tests():
    assert matrix_chain_cost([]) == 0
    assert matrix_chain_cost([10]) == 0
    assert matrix_chain_cost([10, 20]) == 0
    assert matrix_chain_cost([10, 20, 30]) == 6000
    assert matrix_chain_cost([10, 20, 30, 40]) == 18000
    assert matrix_chain_cost([40, 20, 30, 10, 30]) == 26000
    assert matrix_chain_cost([10, 20, 30, 40, 30]) == 30000
    assert matrix_chain_cost([30, 35, 15, 5, 10, 20, 25]) == 15125
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
