"""
Day 29, Task 2 -- Python: subdomain visit counts (dict aggregation).

THE PROBLEM
------------
Each input string is "<count> <domain>", e.g. "9001 discuss.leetcode.com".
Visiting a domain also counts as a visit to every PARENT domain:
"discuss.leetcode.com" counts for "discuss.leetcode.com", "leetcode.com"
and "com".

subdomain_visits(cpdomains) returns a dict {domain: total_visits}.

  subdomain_visits(["9001 discuss.leetcode.com"])
      -> {"discuss.leetcode.com": 9001, "leetcode.com": 9001, "com": 9001}
  subdomain_visits(["5 a.b.com", "7 b.com"])
      -> {"a.b.com": 5, "b.com": 12, "com": 12}
  subdomain_visits([]) -> {}

HOW TO WORK THROUGH THIS
-------------------------
Split each entry once on the space, then walk the dotted labels: for every
suffix starting at label i, ".".join(labels[i:]) is a domain to credit.

Run: python3 subdomain_visit_counts.py
"""


def subdomain_visits(cpdomains: list) -> dict:
    totals = {}
    for entry in cpdomains:
        count, domain = entry.split(" ", 1)
        count = int(count)
        labels = domain.split(".")
        for i in range(len(labels)):
            name = ".".join(labels[i:])
            totals[name] = totals.get(name, 0) + count
    return totals


def _run_tests():
    assert subdomain_visits(["9001 discuss.leetcode.com"]) == {
        "discuss.leetcode.com": 9001, "leetcode.com": 9001, "com": 9001}
    assert subdomain_visits(["5 a.b.com", "7 b.com"]) == {
        "a.b.com": 5, "b.com": 12, "com": 12}
    assert subdomain_visits([]) == {}
    assert subdomain_visits(["3 localhost"]) == {"localhost": 3}
    r = subdomain_visits(["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"])
    assert r == {"google.mail.com": 900, "mail.com": 901, "com": 951,
                 "yahoo.com": 50, "intel.mail.com": 1, "wiki.org": 5, "org": 5}
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
