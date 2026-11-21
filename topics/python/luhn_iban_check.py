"""
Day 61, Task 1 -- Python: check digits -- Luhn (cards) and ISO 13616 / mod-97 (IBAN).

THE PROBLEM
------------
Check digits catch typos before anything hits a database. Implement both classic
schemes with plain integer / string work (no third-party libraries, no regex needed).

1) luhn_valid(number) -> bool
   `number` is a string of digits that may contain spaces or hyphens as separators
   ("4539 1488 0343 6467", "79927398713"). Strip separators; any OTHER character, or
   fewer than 2 digits after stripping, makes it invalid (return False, don't raise).
   Luhn: from the RIGHTMOST digit going left, double every SECOND digit (the 2nd, 4th,
   ...); if a doubled value is > 9 subtract 9; the number is valid iff the total of all
   digits is divisible by 10.

2) luhn_check_digit(payload) -> str
   Given the digits WITHOUT the final check digit (a non-empty digit string, no
   separators), return the single check digit "0".."9" that makes payload + digit
   Luhn-valid. luhn_check_digit("7992739871") -> "3".

3) iban_valid(iban) -> bool
   Accept spaces anywhere and lower-case letters. After removing spaces and upper-casing:
     - it must be 15..34 characters, only A-Z and 0-9;
     - chars 0-1 are letters (country), chars 2-3 are digits (check digits);
     - the length must match COUNTRY_LENGTHS for that country (unknown country -> False);
     - move the first 4 chars to the END, replace every letter by two digits
       (A=10, B=11, ..., Z=35), read the result as an integer: valid iff it mod 97 == 1.
   Do the mod-97 piecewise (process the digit string in chunks, carrying the remainder)
   instead of building one huge int -- that is how it must be done in languages without
   big integers, and it's the point of the exercise.

4) iban_format(iban) -> str
   Normalised "print format": upper case, groups of 4 separated by single spaces
   ("gb82west12345698765432" -> "GB82 WEST 1234 5698 7654 32"). No validation here.

Hint for 3: remainder = 0; for each digit d: remainder = (remainder * 10 + d) % 97.
Hint for 2: try all ten digits, or compute it directly from the Luhn sum of payload + "0".

Run: python3 luhn_iban_check.py
"""

COUNTRY_LENGTHS = {
    "AT": 20, "BE": 16, "CH": 21, "DE": 22, "ES": 24, "FR": 27,
    "GB": 22, "IT": 27, "NL": 18, "NO": 15, "PL": 28, "AM": None,  # AM: no IBAN
}


_DIGITS = "0123456789"
_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _luhn_sum(digits):
    total = 0
    for pos, ch in enumerate(reversed(digits)):
        d = ord(ch) - 48
        if pos % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


def luhn_valid(number):
    digits = []
    for ch in number:
        if ch in " -":
            continue
        if ch not in _DIGITS:
            return False
        digits.append(ch)
    if len(digits) < 2:
        return False
    return _luhn_sum(digits) % 10 == 0


def luhn_check_digit(payload):
    if not payload or any(ch not in _DIGITS for ch in payload):
        raise ValueError("payload must be a non-empty digit string")
    return str((10 - _luhn_sum(payload + "0") % 10) % 10)


def _mod97(digit_string, chunk=9):
    rem = 0
    for i in range(0, len(digit_string), chunk):
        part = digit_string[i:i + chunk]
        rem = int(str(rem) + part) % 97
    return rem


def iban_valid(iban):
    s = iban.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    if any(ch not in _DIGITS and ch not in _UPPER for ch in s):
        return False
    if s[0] not in _UPPER or s[1] not in _UPPER or s[2] not in _DIGITS or s[3] not in _DIGITS:
        return False
    expected = COUNTRY_LENGTHS.get(s[:2])
    if expected is None or len(s) != expected:
        return False
    rearranged = s[4:] + s[:4]
    digits = "".join(ch if ch in _DIGITS else str(_UPPER.index(ch) + 10) for ch in rearranged)
    return _mod97(digits) == 1


def iban_format(iban):
    s = iban.replace(" ", "").upper()
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


def _run_tests():
    assert luhn_valid("79927398713") is True
    assert luhn_valid("79927398710") is False
    assert luhn_valid("4539 1488 0343 6467") is True
    assert luhn_valid("4539-1488-0343-6467") is True
    assert luhn_valid("4539 1488 0343 6468") is False
    assert luhn_valid("0") is False            # too short
    assert luhn_valid("00") is True            # all zeros, 2 digits
    assert luhn_valid("") is False
    assert luhn_valid("4539x1488") is False
    assert luhn_valid("18") is True
    assert luhn_valid("59") is True
    assert luhn_valid("91") is True

    assert luhn_check_digit("7992739871") == "3"
    assert luhn_check_digit("453914880343646") == "7"
    assert luhn_check_digit("0") == "0"
    assert luhn_check_digit("1") == "8"
    import random
    rng = random.Random(61)
    for _ in range(300):
        p = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 25)))
        d = luhn_check_digit(p)
        assert len(d) == 1 and d.isdigit()
        assert luhn_valid(p + d), p
        # any single-digit typo is detected
        i = rng.randrange(len(p) + 1)
        s = p + d
        wrong = str((int(s[i]) + rng.randint(1, 9)) % 10)
        assert not luhn_valid(s[:i] + wrong + s[i + 1:]), (s, i)

    assert iban_valid("GB82 WEST 1234 5698 7654 32") is True
    assert iban_valid("gb82west12345698765432") is True
    assert iban_valid("GB82 WEST 1234 5698 7654 33") is False
    assert iban_valid("DE89 3704 0044 0532 0130 00") is True
    assert iban_valid("NL91 ABNA 0417 1643 00") is True
    assert iban_valid("NO93 8601 1117 947") is True
    assert iban_valid("FR14 2004 1010 0505 0001 3M02 606") is True
    assert iban_valid("BE68 5390 0754 7034") is True
    assert iban_valid("DE89 3704 0044 0532 0130 0") is False      # wrong length for DE
    assert iban_valid("XX82 WEST 1234 5698 7654 32") is False     # unknown country
    assert iban_valid("AM12 3456 7890 1234 5") is False          # country without IBAN
    assert iban_valid("GB8X WEST 1234 5698 7654 32") is False     # check digits not digits
    assert iban_valid("GB82-WEST-1234-5698-7654-32") is False     # hyphen not allowed
    assert iban_valid("") is False
    # swapping two adjacent characters is caught
    assert iban_valid("GB82 WEST 1234 5698 7654 23") is False

    assert iban_format("gb82west12345698765432") == "GB82 WEST 1234 5698 7654 32"
    assert iban_format("  NO93 8601 1117 947 ") == "NO93 8601 1117 947"
    assert iban_format("be68539007547034") == "BE68 5390 0754 7034"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
