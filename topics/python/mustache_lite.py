"""
Day 60, Task 10 -- Python: a tiny logic-less template engine (a Mustache subset).

THE PROBLEM
------------
Implement render(template, context) -> str WITHOUT importing re, string.Template,
chevron/pystache or any template library. Tags are delimited by {{ and }}; whitespace
just inside the braces is ignored ({{ name }} == {{name}}).

  {{name}}        the value, converted with str() and HTML-ESCAPED:
                  & -> &amp;   < -> &lt;   > -> &gt;   " -> &quot;   ' -> &#39;
                  A missing name (or None) renders as "".
  {{{name}}}      the value, NOT escaped.     {{& name}} is the same thing.
  {{! anything}}  a comment: renders nothing.
  {{#name}}...{{/name}}   a SECTION:
                  - value is a list/tuple: render the inside once per item, with the
                    item pushed on the context stack (empty list -> nothing);
                  - value is falsy (missing, None, False, 0, "", {}): render nothing;
                  - value is a dict: render the inside once with the dict pushed;
                  - any other truthy value: render the inside once with it pushed.
  {{^name}}...{{/name}}   an INVERTED section: render the inside once (nothing pushed)
                  exactly when the section above would render nothing.

Name lookup uses a CONTEXT STACK (the initial context at the bottom):
  - "."           is the top of the stack itself (handy inside a list of strings);
  - "a"           the innermost dict on the stack that HAS key "a" wins, even if its
                  value is falsy; a non-dict stack entry is skipped;
  - "a.b.c"       look up "a" as above, then descend with ["b"], ["c"]; if any step is
                  not a dict or lacks the key, the result is missing ("").
Sections nest, and the same name may be nested inside itself.
No standalone-line whitespace stripping: text outside tags is copied verbatim.

Errors -> ValueError: a "{{" with no closing "}}" (or "{{{" with no "}}}"), an empty tag
name, a {{/x}} that does not close the innermost open section, or a section still open
at the end of the template.

Examples:
  render("Hi {{name}}!", {"name": "<Ann>"})                    -> "Hi &lt;Ann&gt;!"
  render("{{#items}}[{{.}}]{{/items}}", {"items": [1, 2]})     -> "[1][2]"
  render("{{^items}}none{{/items}}", {"items": []})            -> "none"

Hint: two phases. Tokenize into ("text", s) / ("var", name, escape) / ("open", name,
inverted) / ("close", name) tokens, then parse them into a tree with a stack (this is
where unbalanced sections are caught), then render the tree recursively with the
context stack as a list.

Run: python3 mustache_lite.py
"""


_MISSING = object()


def _escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


def _tokenize(template):
    tokens = []
    i, n = 0, len(template)
    while i < n:
        j = template.find("{{", i)
        if j < 0:
            tokens.append(("text", template[i:]))
            break
        if j > i:
            tokens.append(("text", template[i:j]))
        if template.startswith("{{{", j):
            end = template.find("}}}", j + 3)
            if end < 0:
                raise ValueError("unclosed {{{ tag at %d" % j)
            name = template[j + 3:end].strip()
            if not name:
                raise ValueError("empty tag name at %d" % j)
            tokens.append(("var", name, False))
            i = end + 3
            continue
        end = template.find("}}", j + 2)
        if end < 0:
            raise ValueError("unclosed {{ tag at %d" % j)
        body = template[j + 2:end].strip()
        i = end + 2
        if not body:
            raise ValueError("empty tag name at %d" % j)
        sigil = body[0]
        if sigil == "!":
            continue
        if sigil in "#^/&":
            name = body[1:].strip()
            if not name:
                raise ValueError("empty tag name at %d" % j)
            if sigil == "#":
                tokens.append(("open", name, False))
            elif sigil == "^":
                tokens.append(("open", name, True))
            elif sigil == "/":
                tokens.append(("close", name))
            else:
                tokens.append(("var", name, False))
        else:
            tokens.append(("var", body, True))
    return tokens


def _parse(tokens):
    root = []
    stack = [("", False, root)]       # (name, inverted, children)
    for tok in tokens:
        kind = tok[0]
        if kind == "open":
            node = ("section", tok[1], tok[2], [])
            stack[-1][2].append(node)
            stack.append((tok[1], tok[2], node[3]))
        elif kind == "close":
            if len(stack) == 1 or stack[-1][0] != tok[1]:
                raise ValueError("unexpected closing tag {{/%s}}" % tok[1])
            stack.pop()
        else:
            stack[-1][2].append(tok)
    if len(stack) > 1:
        raise ValueError("unclosed section {{#%s}}" % stack[-1][0])
    return root


def _lookup(name, stack):
    if name == ".":
        return stack[-1]
    parts = name.split(".")
    value = _MISSING
    for frame in reversed(stack):
        if isinstance(frame, dict) and parts[0] in frame:
            value = frame[parts[0]]
            break
    if value is _MISSING:
        return _MISSING
    for part in parts[1:]:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return _MISSING
    return value


def _render_nodes(nodes, stack, out):
    for node in nodes:
        kind = node[0]
        if kind == "text":
            out.append(node[1])
        elif kind == "var":
            value = _lookup(node[1], stack)
            if value is _MISSING or value is None:
                continue
            s = str(value)
            out.append(_escape(s) if node[2] else s)
        else:  # section
            _, name, inverted, children = node
            value = _lookup(name, stack)
            if value is _MISSING:
                value = None
            if isinstance(value, (list, tuple)):
                empty = len(value) == 0
            else:
                empty = not value
            if inverted:
                if empty:
                    _render_nodes(children, stack, out)
            elif not empty:
                items = value if isinstance(value, (list, tuple)) else [value]
                for item in items:
                    stack.append(item)
                    _render_nodes(children, stack, out)
                    stack.pop()


def render(template, context):
    tree = _parse(_tokenize(template))
    out = []
    _render_nodes(tree, [context], out)
    return "".join(out)


def _run_tests():
    assert render("", {}) == ""
    assert render("plain text", {}) == "plain text"
    assert render("Hi {{name}}!", {"name": "<Ann>"}) == "Hi &lt;Ann&gt;!"
    assert render("Hi {{ name }}!", {"name": "Bo"}) == "Hi Bo!"
    assert render("{{x}}", {"x": "a&b\"c'd"}) == "a&amp;b&quot;c&#39;d"
    assert render("{{{x}}}|{{& x}}", {"x": "<b>"}) == "<b>|<b>"
    assert render("[{{missing}}]", {}) == "[]"
    assert render("[{{n}}]", {"n": None}) == "[]"
    assert render("{{n}} {{f}} {{t}}", {"n": 0, "f": 1.5, "t": True}) == "0 1.5 True"
    assert render("a{{! ignore me }}b", {}) == "ab"
    assert render("{{#items}}[{{.}}]{{/items}}", {"items": [1, 2]}) == "[1][2]"
    assert render("{{#items}}x{{/items}}", {"items": []}) == ""
    assert render("{{^items}}none{{/items}}", {"items": []}) == "none"
    assert render("{{^items}}none{{/items}}", {"items": [0]}) == ""
    for falsy in (None, False, 0, "", {}):
        assert render("{{#v}}yes{{/v}}{{^v}}no{{/v}}", {"v": falsy}) == "no", falsy
    assert render("{{#v}}yes{{/v}}{{^v}}no{{/v}}", {}) == "no"
    assert render("{{#v}}<{{.}}>{{/v}}", {"v": "a&b"}) == "<a&amp;b>"
    assert render("{{#u}}{{name}} ({{age}}){{/u}}", {"u": {"name": "Ann", "age": 30}}) \
        == "Ann (30)"
    people = {"people": [{"name": "Ann", "pets": ["cat", "dog"]},
                         {"name": "Bo", "pets": []}]}
    t = "{{#people}}{{name}}:{{#pets}} {{.}}{{/pets}}{{^pets}} -{{/pets}};{{/people}}"
    assert render(t, people) == "Ann: cat dog;Bo: -;"
    # outer names are visible inside sections; inner keys shadow outer ones
    ctx = {"greeting": "hi", "name": "outer", "list": [{"name": "in1"}, {"x": 1}]}
    assert render("{{#list}}{{greeting}} {{name}}|{{/list}}", ctx) == "hi in1|hi outer|"
    # a falsy value in an inner dict still shadows the outer key
    assert render("{{#o}}[{{k}}]{{/o}}", {"k": "outer", "o": {"k": ""}}) == "[]"
    # dotted names
    d = {"a": {"b": {"c": "deep"}}, "s": "str"}
    assert render("{{a.b.c}}|{{a.x.c}}|{{s.len}}|{{a.b}}", d) \
        == "deep|||{&#39;c&#39;: &#39;deep&#39;}"
    assert render("{{#a.b}}{{c}}{{/a.b}}", d) == "deep"
    assert render("{{#a}}{{#b}}{{c}}-{{a.b.c}}{{/b}}{{/a}}", d) == "deep-deep"
    # same section name nested inside itself
    assert render("{{#x}}{{#x}}{{y}}{{/x}}{{/x}}", {"x": {"x": {"y": "in"}, "y": "out"}}) \
        == "in"
    assert render("a\n{{#s}}\nb\n{{/s}}\nc", {"s": True}) == "a\n\nb\n\nc"
    assert render("{x} {{n}}} }}", {"n": 1}) == "{x} 1} }}"
    big = render("{{#r}}{{.}},{{/r}}", {"r": list(range(2000))})
    assert big == "".join("%d," % i for i in range(2000))
    for bad in ["{{name", "{{{name}}", "{{}}", "{{#a}}x", "{{#a}}{{/b}}", "x{{/a}}",
                "{{#a}}{{#b}}{{/a}}{{/b}}", "{{ }}"]:
        try:
            render(bad, {"a": 1, "b": 1, "name": 1})
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
