"""
Day 25, Task 3 -- Python: multiply two big numbers given as strings.

THE PROBLEM
------------
multiply_strings(a, b) takes two non-negative integers written as decimal
strings and returns their product as a string. You may NOT convert a whole
string with int() or use big-int multiplication on the inputs (converting
single digits is fine). Inputs have no leading zeros except "0" itself;
the result must not have leading zeros either.

  multiply_strings("123", "456") == "56088"
  multiply_strings("0", "99")    == "0"

HOW TO WORK THROUGH THIS
-------------------------
Schoolbook multiplication: digit i of a (from the right) times digit j of b
lands at position i + j of a result array; add, then carry from low to high.

Run: python3 multiply_strings.py
"""


def multiply_strings(a: str, b: str) -> str:
    if a == "0" or b == "0":
        return "0"
    res = [0] * (len(a) + len(b))
    for i, ca in enumerate(reversed(a)):
        for j, cb in enumerate(reversed(b)):
            res[i + j] += (ord(ca) - 48) * (ord(cb) - 48)
    carry = 0
    for k in range(len(res)):
        total = res[k] + carry
        res[k] = total % 10
        carry = total // 10
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return "".join(str(d) for d in reversed(res))


def _run_tests():
    assert multiply_strings("2", "3") == "6"
    assert multiply_strings("123", "456") == "56088"
    assert multiply_strings("0", "99") == "0"
    assert multiply_strings("99", "0") == "0"
    assert multiply_strings("999", "999") == "998001"
    assert multiply_strings("1", "1") == "1"
    x, y = "123456789012345678901234567890", "987654321098765432109876543210"
    assert multiply_strings(x, y) == str(int(x) * int(y))
    assert multiply_strings("1000", "1000") == "1000000"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
