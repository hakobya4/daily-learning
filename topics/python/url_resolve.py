"""
Day 62, Task 2 -- Python: RFC 3986 URI splitting and relative-reference resolution.

THE PROBLEM
------------
A browser sees <a href="../g?y#s"> on the page http://a/b/c/d;p?q and must work out the
absolute target. RFC 3986 section 5 defines the algorithm exactly. Implement it
WITHOUT urllib.parse (the tests do not use it either -- urljoin differs in corner cases).

1) split_uri(ref) -> (scheme, authority, path, query, fragment)
   Use the RFC's regular expression from appendix B:
       ^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\\?([^#]*))?(#(.*))?
   Components that are ABSENT are None; present-but-empty ones are "" -- the difference
   matters: "http://a/b?" has query "" while "http://a/b" has query None.
   path is always a string (possibly "").

2) unsplit_uri(scheme, authority, path, query, fragment) -> str
   Section 5.3 "component recomposition": add "scheme:", "//authority", path,
   "?query", "#fragment" only for components that are not None.

3) remove_dot_segments(path) -> str
   Section 5.2.4: the input-buffer / output-buffer loop (rules A to E). Examples:
       "/a/b/c/./../../g"  -> "/a/g"
       "mid/content=5/../6" -> "mid/6"
       "/../g" -> "/g"      "/./" -> "/"      "/a/.." -> "/"      "." -> ""
   Do NOT take shortcuts with str.split/normpath -- implement the five rules, they
   are what make ".." at the root and trailing "." / ".." come out right.

4) resolve(base, ref) -> str
   Section 5.2.2 (strict, i.e. a ref with the SAME scheme is NOT treated as relative),
   using section 5.2.3 "merge" when the ref path is relative:
     - if the base has an authority and an empty path, merge gives "/" + ref path;
     - otherwise, everything in the base path up to and including the last "/",
       followed by the ref path.
   The base is always absolute (has a scheme).

Run: python3 url_resolve.py
"""


def split_uri(ref):
    raise NotImplementedError


def unsplit_uri(scheme, authority, path, query, fragment):
    raise NotImplementedError


def remove_dot_segments(path):
    raise NotImplementedError


def resolve(base, ref):
    raise NotImplementedError


def _run_tests():
    assert split_uri("http://a/b/c/d;p?q") == ("http", "a", "/b/c/d;p", "q", None)
    assert split_uri("http://a/b?") == ("http", "a", "/b", "", None)
    assert split_uri("http://a/b") == ("http", "a", "/b", None, None)
    assert split_uri("//host") == (None, "host", "", None, None)
    assert split_uri("#") == (None, None, "", None, "")
    assert split_uri("mailto:x@y.z") == ("mailto", None, "x@y.z", None, None)
    assert split_uri("") == (None, None, "", None, None)
    assert split_uri("foo://u@ex.com:8042/over/there?name=ferret#nose") == \
        ("foo", "u@ex.com:8042", "/over/there", "name=ferret", "nose")
    for u in ["http://a/b?", "http://a/b#", "//h", "a/b", "", "?q", "s:", "s://"]:
        assert unsplit_uri(*split_uri(u)) == u, u

    assert remove_dot_segments("/a/b/c/./../../g") == "/a/g"
    assert remove_dot_segments("mid/content=5/../6") == "mid/6"
    assert remove_dot_segments("/../g") == "/g"
    assert remove_dot_segments("/./") == "/"
    assert remove_dot_segments("/a/..") == "/"
    assert remove_dot_segments("/a/.") == "/a/"
    assert remove_dot_segments(".") == ""
    assert remove_dot_segments("..") == ""
    assert remove_dot_segments("../a/./b/../c") == "a/c"
    assert remove_dot_segments("/a/b/...") == "/a/b/..."
    assert remove_dot_segments("/a//../b") == "/a/b"
    assert remove_dot_segments("") == ""

    base = "http://a/b/c/d;p?q"
    # RFC 3986 section 5.4.1 (normal) and 5.4.2 (abnormal) examples
    examples = {
        "g:h": "g:h", "g": "http://a/b/c/g", "./g": "http://a/b/c/g",
        "g/": "http://a/b/c/g/", "/g": "http://a/g", "//g": "http://g",
        "?y": "http://a/b/c/d;p?y", "g?y": "http://a/b/c/g?y",
        "#s": "http://a/b/c/d;p?q#s", "g#s": "http://a/b/c/g#s",
        "g?y#s": "http://a/b/c/g?y#s", ";x": "http://a/b/c/;x",
        "g;x": "http://a/b/c/g;x", "g;x?y#s": "http://a/b/c/g;x?y#s",
        "": "http://a/b/c/d;p?q", ".": "http://a/b/c/", "./": "http://a/b/c/",
        "..": "http://a/b/", "../": "http://a/b/", "../g": "http://a/b/g",
        "../..": "http://a/", "../../": "http://a/", "../../g": "http://a/g",
        "../../../g": "http://a/g", "../../../../g": "http://a/g",
        "/./g": "http://a/g", "/../g": "http://a/g", "g.": "http://a/b/c/g.",
        ".g": "http://a/b/c/.g", "g..": "http://a/b/c/g..", "..g": "http://a/b/c/..g",
        "./../g": "http://a/b/g", "./g/.": "http://a/b/c/g/",
        "g/./h": "http://a/b/c/g/h", "g/../h": "http://a/b/c/h",
        "g;x=1/./y": "http://a/b/c/g;x=1/y", "g;x=1/../y": "http://a/b/c/y",
        "g?y/./x": "http://a/b/c/g?y/./x", "g?y/../x": "http://a/b/c/g?y/../x",
        "g#s/./x": "http://a/b/c/g#s/./x", "g#s/../x": "http://a/b/c/g#s/../x",
        "http:g": "http:g",
    }
    for ref, want in examples.items():
        got = resolve(base, ref)
        assert got == want, (ref, got, want)

    assert resolve("http://a", "b") == "http://a/b"          # empty base path + authority
    assert resolve("http://a?x", "?y") == "http://a?y"
    assert resolve("mailto:x@y", "#top") == "mailto:x@y#top"
    assert resolve("file:///etc/hosts", "passwd") == "file:///etc/passwd"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
