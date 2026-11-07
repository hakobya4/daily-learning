"""
Day 48, Task 2 -- Python: count unique normalized email addresses.

THE PROBLEM
------------
An address is "local@domain". Normalization rules:
  * in the local part, "." is ignored            ("a.b@x.com" == "ab@x.com")
  * in the local part, everything from the first "+" onward is ignored
  * the domain is case-insensitive (lowercase it); the local part is kept as is
    except for the two rules above (it IS case-sensitive here)
  * the domain part is NOT touched by the dot/plus rules
num_unique_emails(emails) returns how many distinct normalized addresses there are.

Run: python3 unique_emails.py
"""


def num_unique_emails(emails):
    raise NotImplementedError


def _run_tests():
    assert num_unique_emails([]) == 0
    assert num_unique_emails(["a@x.com"]) == 1
    assert num_unique_emails(["a.b@x.com", "ab@x.com", "a.b+spam@x.com"]) == 1
    assert num_unique_emails(["a@x.com", "a@y.com"]) == 2
    assert num_unique_emails(["a@X.COM", "a@x.com"]) == 1
    assert num_unique_emails(["Ab@x.com", "ab@x.com"]) == 2
    assert num_unique_emails(["a@x.co.m", "a@xc.o.m"]) == 2
    assert num_unique_emails(["+a@x.com", "+b@x.com"]) == 1
    assert num_unique_emails(["a+b+c@x.com", "a.@x.com", "a@x.com"]) == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
