"""
Day 12, Task 2 -- Python: IPv4 parsing and CIDR membership.

THE PROBLEM
------------
Implement three functions WITHOUT the ipaddress module:

  ip_to_int(ip) -> int
      Parse a dotted-quad such as "192.168.1.10" into a 32-bit integer.
      Raise ValueError unless there are exactly 4 parts, each a decimal
      number 0-255 with no sign, no spaces and no empty parts.

  int_to_ip(n) -> str
      The inverse. Raise ValueError if n is outside 0..2**32-1.

  in_cidr(ip, cidr) -> bool
      cidr looks like "10.0.0.0/8". True if ip falls inside the block.
      /0 matches everything, /32 matches exactly one address. Raise
      ValueError for a prefix outside 0..32. Host bits in the cidr's
      base address are ignored ("10.1.2.3/8" behaves like "10.0.0.0/8").

HOW TO WORK THROUGH THIS
-------------------------
Build a mask: ((1 << 32) - 1) ^ ((1 << (32 - prefix)) - 1). Then compare
ip & mask with base & mask. Watch the prefix == 0 case.

Run: python3 ipv4_cidr.py
"""


def ip_to_int(ip):
    raise NotImplementedError


def int_to_ip(n):
    raise NotImplementedError


def in_cidr(ip, cidr):
    raise NotImplementedError


def _run_tests() -> None:
    assert ip_to_int("0.0.0.0") == 0
    assert ip_to_int("255.255.255.255") == 2**32 - 1
    assert ip_to_int("192.168.1.10") == 3232235786
    assert int_to_ip(3232235786) == "192.168.1.10"
    assert int_to_ip(0) == "0.0.0.0"
    for n in (0, 1, 16909060, 2**32 - 1):
        assert ip_to_int(int_to_ip(n)) == n
    for bad in ("1.2.3", "1.2.3.4.5", "256.1.1.1", "1.2.3.-4", "a.b.c.d",
                "1..3.4", " 1.2.3.4", "1.2.3.4 ", ""):
        try:
            ip_to_int(bad)
            assert False, f"should reject {bad!r}"
        except ValueError:
            pass
    for bad in (-1, 2**32):
        try:
            int_to_ip(bad)
            assert False
        except ValueError:
            pass
    assert in_cidr("10.200.3.4", "10.0.0.0/8") is True
    assert in_cidr("11.0.0.1", "10.0.0.0/8") is False
    assert in_cidr("192.168.1.77", "192.168.1.64/26") is True
    assert in_cidr("192.168.1.128", "192.168.1.64/26") is False
    assert in_cidr("8.8.8.8", "0.0.0.0/0") is True
    assert in_cidr("1.2.3.4", "1.2.3.4/32") is True
    assert in_cidr("1.2.3.5", "1.2.3.4/32") is False
    assert in_cidr("10.9.9.9", "10.1.2.3/8") is True
    try:
        in_cidr("1.2.3.4", "1.2.3.4/33")
        assert False
    except ValueError:
        pass
    print("All ipv4_cidr tests passed.")


if __name__ == "__main__":
    _run_tests()
